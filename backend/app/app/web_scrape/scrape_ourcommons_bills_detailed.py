import os
import datetime
from selenium import webdriver
import requests
import time
import json
import glob
from DirectoryHandler import DirectoryHandler

"https://www.parl.ca/Content/Bills/441/Private/S-206/S-206_1/S-206_E.xml"
"https://www.parl.ca/Content/Bills/441/Government/C-3/C-3_1/C-3_E.xml"
"https://www.parl.ca/Content/Bills/412/Private/C-670/C-670_1/C-670-E.xml"
"https://www.parl.ca/Content/Bills/402/Government/S-2/S-2_1/S-2-e.xml"


def scrape_bill_text():
    """Retrieves bill text for each bill in bill list (tries reading_no 1, 2, 3, 4).

    Returns
    -------
    Nothing

    """
    base_url1 = r"https://www.parl.ca/Content/Bills/{}{}/{}/{}/{}_{}/{}_E.xml"
    base_url2 = r"https://www.parl.ca/Content/Bills/{}{}/{}/{}/{}_{}/{}-e.xml"
    base_urls = [base_url1, base_url2]

    # Preamble, folder locations
    dh_bill_summary = DirectoryHandler("bills summary")
    dh_bill_detail = DirectoryHandler("bills detail")
    dh_bill_detail.load_meta_file()
    dh_bill_detail.file_existing()

    save_dir_bills_summary = dh_bill_summary.path_of_interest
    save_dir_bills_detail = dh_bill_detail.path_of_interest

    json_file = glob.glob(os.path.join(save_dir_bills_summary, "*.json"))

    ################################################################################################################
    # Open summary json
    with open(json_file[0], encoding="utf-8") as f:
        data = f.read()
        structure = json.loads(data)
        # d = json.load(f)

    link_lst = []
    file_lst = []
    for each_item in structure:
        parl_no = each_item.get("ParliamentNumber")
        parl_session = each_item.get("SessionNumber")
        bill_no = each_item.get("NumberCode")

        type_whole = each_item.get("BillDocumentTypeNameEn")
        if "private" in type_whole.lower():
            bill_type = "Private"
        else:
            bill_type = "Government"

        for each_url in base_urls:
            for reading_no in [1, 2, 3, 4]:
                link_lst.append(each_url.format(parl_no, parl_session, bill_type, bill_no, bill_no, reading_no, bill_no))
                file_lst.append(f"{parl_no}_{parl_session}_{bill_no}_{reading_no}.xml")

    print(f"Potential bill readings: {len(link_lst)}")

    # open browser
    try:
        driver = webdriver.Chrome()
    except:
        raise RuntimeError("failed to initialize driver")

    failure_lst = []
    output_list = []

    # Retrieve bill files
    for idx, each_xml_link in enumerate(link_lst):
        print(f"Loop {idx} of {len(link_lst)}")

        # get a filename from parl session
        fn = file_lst[idx]
        fp = os.path.join(save_dir_bills_detail, fn)
        # print(fp)

        if os.path.exists(fp):
            continue
        else:
            try:
                status_code = None
                max_tries = 5
                cur_try = 0

                while cur_try < max_tries and status_code != requests.codes.ok:
                    response = requests.get(each_xml_link)
                    status_code = response.status_code
                    cur_try += 1
                    time.sleep(0.5)
                    print(f"{each_xml_link}\ttry {cur_try}\tcode {response.status_code}")

                    if response.status_code == 404:
                        break

                if response.status_code == requests.codes.ok:
                    with open(fp, 'wb') as handle:
                        handle.write(response.content)
                    output_list.append(fn)
                else:
                    failure_lst.append(each_xml_link)
                    with open(os.path.join(save_dir_bills_detail, "int_failures.txt"), 'a') as f:
                        f.write(f"{failure_lst[-1]}\n")

                    raise RuntimeWarning(f"couldn't get {each_xml_link}")
            except Exception as e:
                print(f"couldn't get {each_xml_link} ({e})")

    driver.close()

    with open(os.path.join(save_dir_bills_detail, 'failures.txt'), 'w') as f:
        for line in failure_lst:
            f.write(f"{line}\n")

    dh_bill_detail.create_meta_file(
        source_date=datetime.datetime.now(),
        source_name="LegisInfo Bills Detailed",
        source_dict={
            "url": "https://www.parl.ca/LegisInfo/en/bills/json?advancedview=true&parlsession=all",
            "filenames": output_list
        }
    )

