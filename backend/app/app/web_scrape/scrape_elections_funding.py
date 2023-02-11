import os
import datetime
from selenium import webdriver
import requests
import time
from DirectoryHandler import DirectoryHandler
import zipfile
import pandas as pd


def scrape_election_funding():
    """Retrieves contributions to all political entities from January 2004 to present. Updated weekly. As reviewed.

    Returns
    -------
    Nothing

    """
    base_url = r"https://www.elections.ca/fin/oda/od_cntrbtn_audt_e.zip"

    # Preamble, folder locations
    dh_funding = DirectoryHandler("ecanada_contrib")
    dh_funding.load_meta_file()
    dh_funding.file_existing()

    save_dir = dh_funding.path_of_interest

    # open browser
    try:
        driver = webdriver.Chrome()
    except:
        raise RuntimeError("failed to initialize driver")

    # Retrieve contribution file
    zip_link = base_url

    # get a filename
    fn = f"od_cntrbtn_audt_e.zip"
    fn_csv = f"od_cntrbtn_audt_e.csv"
    fp = os.path.join(save_dir, fn)
    fp_csv = os.path.join(save_dir, fn_csv)
    print(fp)

    status_code = None
    max_tries = 10
    cur_try = 0

    while cur_try < max_tries and status_code != requests.codes.ok:
        response = requests.get(zip_link)
        status_code = response.status_code
        cur_try += 1
        time.sleep(5)
        print(f"{zip_link}\ttry {cur_try}\tcode {response.status_code}")

    if response.status_code == requests.codes.ok:
        with open(fp, 'wb') as handle:
            handle.write(response.content)
    else:
        raise RuntimeWarning(f"couldn't get {zip_link}")

    driver.close()

    zf = zipfile.ZipFile(fp)
    df = pd.read_csv(zf.open("PoliticalFinance/" + fn_csv))
    df.to_csv(fp_csv)

    dh_funding.create_meta_file(
        source_date=datetime.datetime.now(),
        source_name="Elections Canada Open Data",
        source_dict={
            "url": base_url,
            "filenames": [fn, fn_csv]
        }
    )



