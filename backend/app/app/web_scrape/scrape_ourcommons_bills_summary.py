import os
import datetime
from selenium import webdriver
import requests
import time
from DirectoryHandler import DirectoryHandler


def scrape_bill_list():
    """Retrieves high-level list of bills (all parliamentary sessions).

    Returns
    -------
    Nothing

    """
    # https://www.parl.ca/LegisInfo/en/bills/json?advancedview=true&parlsession=all
    base_url = r"https://www.parl.ca/LegisInfo/en/bills/json?advancedview=true&parlsession=all"

    # Preamble, folder locations
    dh_bill_summary = DirectoryHandler("bills summary")
    dh_bill_summary.load_meta_file()
    dh_bill_summary.file_existing()

    save_dir_bills_summary = dh_bill_summary.path_of_interest

    # open browser
    try:
        driver = webdriver.Chrome()
    except:
        raise RuntimeError("failed to initialize driver")

    # Retrieve bill summary files
    json_link = base_url

    # get a filename from parl session
    fn = f"all_bills.json"
    fp = os.path.join(save_dir_bills_summary, fn)
    print(fp)

    status_code = None
    max_tries = 10
    cur_try = 0

    while cur_try < max_tries and status_code != requests.codes.ok:
        response = requests.get(json_link)
        status_code = response.status_code
        cur_try += 1
        time.sleep(5)
        print(f"{json_link}\ttry {cur_try}\tcode {response.status_code}")

    if response.status_code == requests.codes.ok:
        with open(fp, 'wb') as handle:
            handle.write(response.content)
    else:
        raise RuntimeWarning(f"couldn't get {json_link}")

    driver.close()

    dh_bill_summary.create_meta_file(
        source_date=datetime.datetime.now(),
        source_name="LegisInfo Bills Summary",
        source_dict={
            "url": base_url,
            "filenames": [fn]
        }
    )



