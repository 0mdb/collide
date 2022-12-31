import os
import pathlib
from selenium import webdriver
import requests
import time
import pandas as pd
import json
import glob

"https://www.parl.ca/Content/Bills/441/Private/S-206/S-206_1/S-206_E.xml"
"https://www.parl.ca/Content/Bills/441/Private/S-206/S-206_3/S-206_E.xml"
"https://www.parl.ca/Content/Bills/441/Private/S-206/S-206_4/S-206_E.xml"

"https://www.parl.ca/Content/Bills/441/Government/C-3/C-3_1/C-3_E.xml"
"https://www.parl.ca/Content/Bills/441/Government/C-3/C-3_2/C-3_E.xml"
"https://www.parl.ca/Content/Bills/441/Government/C-3/C-3_3/C-3_E.xml"
"https://www.parl.ca/Content/Bills/441/Government/C-3/C-3_4/C-3_E.xml"

"https://www.parl.ca/Content/Bills/412/Private/C-670/C-670_1/C-670-E.xml"

"https://www.parl.ca/Content/Bills/402/Government/S-2/S-2_1/S-2-e.xml"
"https://www.parl.ca/Content/Bills/402/Government/S-2/S-2_3/S-2-e.xml"
"https://www.parl.ca/Content/Bills/402/Government/S-2/S-2_4/S-2-e.xml"

base_url = r"https://www.parl.ca/Content/Bills/{}{}/{}/{}/{}_{}/{}_E.xml"
base_url2 = r"https://www.parl.ca/Content/Bills/{}{}/{}/{}/{}_{}/{}-E.xml"

# Preamble, folder locations
project_name = "app"  # collide\backend\app\app
data_dir = "data"
save_dir_bills = "bills"
save_dir_bills_summary = "summary"
save_dir_bills_detail = "detail"

# Folder creation, directories
curr_dir_name = os.path.dirname(__file__)

absolute_project_path = None
for i in pathlib.Path(curr_dir_name).parents:
    if i.name == project_name:
        absolute_project_path = i.absolute()
        break

save_dir_bills = os.path.join(absolute_project_path, data_dir, save_dir_bills)
save_dir_bills_summary = os.path.join(absolute_project_path, data_dir, save_dir_bills, save_dir_bills_summary)

if not os.path.exists(os.path.join(absolute_project_path, data_dir, save_dir_bills, save_dir_bills_detail)):
    os.mkdir(os.path.join(absolute_project_path, data_dir, save_dir_bills, save_dir_bills_detail))
save_dir_bills_detail = os.path.join(absolute_project_path, data_dir, save_dir_bills, save_dir_bills_detail)

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

    for reading_no in [1, 2, 3, 4]:
        link_lst.append(base_url.format(parl_no, parl_session, bill_type, bill_no, bill_no, reading_no, bill_no))
        file_lst.append(f"{parl_no}_{parl_session}_{bill_no}_{reading_no}.xml")
        # f"https://www.parl.ca/Content/Bills/{parl_no}{parl_session}/{bill_type}/{bill_no}/{bill_no}_{reading_no}/{bill_no}_E.xml"

print(f"{len(link_lst)} potential bill readings to pull")

# open browser
try:
    driver = webdriver.Chrome()
except:
    raise RuntimeError("failed to initialize driver")

failure_lst = []
# Retrieve bill files
link_lst.reverse()
for idx, each_xml_link in enumerate(link_lst):

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

meta_df = pd.DataFrame.from_dict({
    "date_scraped": ["2022-12-30T00:00:00+00:00"],
    "source_name": ["LegisInfo Bills Detailed"],
    "source_url": ["https://www.parl.ca/LegisInfo/en/bills/json?advancedview=true&parlsession=all"]
})

meta_df.to_csv(os.path.join(save_dir_bills_detail, "meta.csv"))
