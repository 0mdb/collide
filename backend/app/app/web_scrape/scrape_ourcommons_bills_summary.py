import os
import pathlib
from selenium import webdriver
import requests
import time
import pandas as pd

# https://www.parl.ca/LegisInfo/en/bills/json?advancedview=true&parlsession=all

base_url = r"https://www.parl.ca/LegisInfo/en/bills/json?advancedview=true&parlsession=all"

################################################################################################################

# Preamble, folder locations
project_name = "app"  # collide\backend\app\app
data_dir = "data"
save_dir_bills = "bills"
save_dir_bills_summary = "summary"

# Folder creation, directories
curr_dir_name = os.path.dirname(__file__)

absolute_project_path = None
for i in pathlib.Path(curr_dir_name).parents:
    if i.name == project_name:
        absolute_project_path = i.absolute()
        break

save_dir_bills = os.path.join(absolute_project_path, data_dir, save_dir_bills)
if not os.path.exists(save_dir_bills):
    os.mkdir(save_dir_bills)

if not os.path.exists(os.path.join(absolute_project_path, data_dir, save_dir_bills, save_dir_bills_summary)):
    os.mkdir(os.path.join(absolute_project_path, data_dir, save_dir_bills, save_dir_bills_summary))
save_dir_bills_summary = os.path.join(absolute_project_path, data_dir, save_dir_bills, save_dir_bills_summary)

################################################################################################################

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

meta_df = pd.DataFrame.from_dict({
    "date_scraped": ["2022-12-30T00:00:00+00:00"],
    "source_name": ["LegisInfo Bills Summary"],
    "source_url": [base_url]
})
meta_df.to_csv(os.path.join(save_dir_bills_summary, "meta.csv"))


