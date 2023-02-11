import os
import datetime
from selenium import webdriver
import requests
import time
from DirectoryHandler import DirectoryHandler
import zipfile


def scrape_lobby_records():
    """Retrieves lobby communications and registrations from open data website.

    Registrations: cover Jan21 1996 to Jun30 2008 (under Lobbyist Registration Act).
    As well as Jul02 2008 onward (under Lobbying Act).

    Monthly communication reports: cover oral and arranged communications between lobbyist and Designated Public
    Office Holders (DPOH). Jul02 2008 onward.


    Returns
    -------
    Nothing

    """
    com_url = r"https://lobbycanada.gc.ca/media/mqbbmaqk/communications_ocl_cal.zip"
    reg_url = r"https://lobbycanada.gc.ca/media/zwcjycef/registrations_enregistrements_ocl_cal.zip"

    # Preamble, folder locations
    dh_com = DirectoryHandler("lobby_comms")
    dh_reg = DirectoryHandler("lobby_regs")

    dh_com.load_meta_file()
    dh_com.file_existing()
    com_save_dir = dh_com.path_of_interest

    dh_reg.load_meta_file()
    dh_reg.file_existing()
    reg_save_dir = dh_reg.path_of_interest

    # open browser
    try:
        driver = webdriver.Chrome()
    except:
        raise RuntimeError("failed to initialize driver")

    # Retrieve contribution file
    com_zip_link = com_url
    reg_zip_link = reg_url

    # get a filename
    com_fn = f"communications_ocl_cal.zip"
    com_fp = os.path.join(com_save_dir, com_fn)
    reg_fn = f"registrations_enregistrements_ocl_cal.zip"
    reg_fp = os.path.join(reg_save_dir, reg_fn)

    # com_fn_csv = f"od_cntrbtn_audt_e.csv"
    # com_fp_csv = os.path.join(com_save_dir, fn_csv)
    print(com_fp)
    print(reg_fp)

    # RETRIEVE COMMUNICATION FILE
    status_code = None
    max_tries = 5
    cur_try = 0

    while cur_try < max_tries and status_code != requests.codes.ok:
        response = requests.get(com_zip_link)
        status_code = response.status_code
        cur_try += 1
        time.sleep(5)
        print(f"{com_zip_link}\ttry {cur_try}\tcode {response.status_code}")

    if response.status_code == requests.codes.ok:
        with open(com_fp, 'wb') as handle:
            handle.write(response.content)
    else:
        raise RuntimeWarning(f"couldn't get {com_zip_link}")

    # RETRIEVE REGISTRATION FILE
    status_code = None
    max_tries = 5
    cur_try = 0

    while cur_try < max_tries and status_code != requests.codes.ok:
        response = requests.get(reg_zip_link)
        status_code = response.status_code
        cur_try += 1
        time.sleep(5)
        print(f"{reg_zip_link}\ttry {cur_try}\tcode {response.status_code}")

    if response.status_code == requests.codes.ok:
        with open(reg_fp, 'wb') as handle:
            handle.write(response.content)
    else:
        raise RuntimeWarning(f"couldn't get {reg_zip_link}")

    driver.close()

    ##########################################

    with zipfile.ZipFile(com_fp, 'r') as zip_ref:
        zip_ref.extractall(com_save_dir)

    with zipfile.ZipFile(reg_fp, 'r') as zip_ref:
        zip_ref.extractall(reg_save_dir)

    com_file_n_dir_names = os.listdir(dh_com.path_of_interest)
    com_file_names = [f for f in com_file_n_dir_names if os.path.isfile(os.path.join(dh_com.path_of_interest, f))]

    reg_file_n_dir_names = os.listdir(dh_reg.path_of_interest)
    reg_file_names = [f for f in reg_file_n_dir_names if os.path.isfile(os.path.join(dh_reg.path_of_interest, f))]

    dh_com.create_meta_file(
        source_date=datetime.datetime.now(),
        source_name="Office of the Commissioner of Lobbying of Canada, Monthly Communication Reports",
        source_dict={
            "url": com_url,
            "filenames": com_file_names
        }
    )

    dh_reg.create_meta_file(
        source_date=datetime.datetime.now(),
        source_name="Office of the Commissioner of Lobbying of Canada, Lobbying Registrations",
        source_dict={
            "url": reg_url,
            "filenames": reg_file_names
        }
    )



