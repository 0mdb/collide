import os
import datetime
import pandas as pd
from selenium import webdriver
import requests
import time
import glob
from DirectoryHandler import DirectoryHandler


def scrape_vote_details():
    """Retrieves vote details (voter name, vote) for each vote in vote list.

    Returns
    -------
    Nothing

    """
    # https://www.ourcommons.ca/members/en/votes/44/1/244/xml

    # Preamble, folder locations
    dh_vote_summary = DirectoryHandler("votes summary")
    dh_vote_detail = DirectoryHandler("votes detail")
    dh_vote_detail.load_meta_file()
    dh_vote_detail.file_existing()

    save_dir_votes_summary = dh_vote_summary.path_of_interest
    save_dir_votes_detail = dh_vote_detail.path_of_interest
    output_list = []

    # Retrieve list of parliament, session, vote number
    lst_sess_csv = glob.glob(os.path.join(save_dir_votes_summary, "*.csv"))
    lst_sess_csv = [x for x in lst_sess_csv if os.path.basename(x) != "meta.csv"]
    parl_no_lst = []
    parl_session_lst = []
    parl_vote_lst = []

    for each_file in lst_sess_csv:
        df = pd.read_csv(each_file)
        parl_no_lst = parl_no_lst + (df["Parliament"].to_list())
        parl_session_lst = parl_session_lst + (df["Session"].to_list())
        parl_vote_lst = parl_vote_lst + (df["Vote Number"].to_list())

    base_url = r"https://www.ourcommons.ca/members/en/votes/{}/{}/{}/xml"

    # open browser
    try:
        driver = webdriver.Chrome()
    except:
        raise RuntimeError("failed to initialize driver")

    # Retrieve vote summary files
    for x, y, z in zip(parl_no_lst, parl_session_lst, parl_vote_lst):
        xml_link = base_url.format(x, y, z)

        # get a filename from code
        fn = f"{x}_{y}_{z}.xml"
        fp = os.path.join(save_dir_votes_detail, fn)
        print(fp)

        if os.path.exists(fp):
            continue
        else:

            try:
                status_code = None
                max_tries = 10
                cur_try = 0

                while cur_try < max_tries and status_code != requests.codes.ok:
                    response = requests.get(xml_link)
                    status_code = response.status_code
                    cur_try += 1
                    time.sleep(5)
                    print(f"{xml_link}\ttry {cur_try}\tcode {response.status_code}")

                if response.status_code == requests.codes.ok:
                    with open(fp, 'wb') as handle:
                        handle.write(response.content)
                    output_list.append(fn)
                else:
                    print(f"couldn't get {xml_link}")
            except Exception as e:
                print(f"couldn't get {xml_link} ({e})")

    driver.close()

    dh_vote_detail.create_meta_file(
        source_date=datetime.datetime.now(),
        source_name="Our Commons Votes Detailed",
        source_dict={
            "url": "https://www.ourcommons.ca/members/en/votes",
            "filenames": output_list
        }
    )
