import os
import datetime
from selenium import webdriver
import requests
import time
from DirectoryHandler import DirectoryHandler


def scrape_vote_list(parl_sessions):
    """Retrieves high-level list of votes for given parliamentary sessions.

    Parameters
    ----------
    parl_sessions: list of str

    Returns
    -------
    Nothing

    """
    # https://www.ourcommons.ca/members/en/votes?parlSession=44-1

    base_url = r"https://www.ourcommons.ca/members/en/votes/csv?parlSession={}"

    # Preamble, folder locations
    dh_vote_summary = DirectoryHandler("votes summary")
    dh_vote_summary.load_meta_file()
    dh_vote_summary.file_existing()

    save_dir_votes_summary = dh_vote_summary.path_of_interest
    output_list = []

    # open browser
    try:
        driver = webdriver.Chrome()
    except:
        raise RuntimeError("failed to initialize driver")

    # Retrieve vote summary files
    for every_session in parl_sessions:
        csv_link = base_url.format(every_session)

        # get a filename from parl session
        fn = f"{every_session}.csv"
        fp = os.path.join(save_dir_votes_summary, fn)
        print(fp)

        status_code = None
        max_tries = 5
        cur_try = 0

        while cur_try < max_tries and status_code != requests.codes.ok:
            response = requests.get(csv_link)
            status_code = response.status_code
            cur_try += 1
            time.sleep(5)
            print(f"{csv_link}\ttry {cur_try}\tcode {response.status_code}")

        if response.status_code == requests.codes.ok:
            with open(fp, 'wb') as handle:
                handle.write(response.content)
            output_list.append(fn)
        else:
            print(f"couldn't get {csv_link}")

    driver.close()

    dh_vote_summary.create_meta_file(
        source_date=datetime.datetime.now(),
        source_name="Our Commons Votes Summary",
        source_dict={
            "url": "https://www.ourcommons.ca/members/en/votes",
            "filenames": output_list
        }
    )

