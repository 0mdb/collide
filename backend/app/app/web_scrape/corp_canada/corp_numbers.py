from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import os
import pathlib
import pandas as pd
import glob
import time
import re

# Preamble, folder locations
project_name = "app"  # collide\backend\app\app
data_dir = "data"
save_dir_corp_no = "corp_no"
tsx_list_dir = "corp_tsx"

# Folder creation, directories
curr_dir_name = os.path.dirname(__file__)

absolute_project_path = None
for i in pathlib.Path(curr_dir_name).parents:
    if i.name == project_name:
        absolute_project_path = i.absolute()
        break

if not os.path.exists(os.path.join(absolute_project_path, data_dir)):
    os.mkdir(os.path.join(absolute_project_path, data_dir))

if not os.path.exists(os.path.join(absolute_project_path, data_dir, save_dir_corp_no)):
    os.mkdir(os.path.join(absolute_project_path, data_dir, save_dir_corp_no))
save_dir_corp_no = os.path.join(absolute_project_path, data_dir, save_dir_corp_no)

tsx_dir = os.path.join(absolute_project_path, data_dir, tsx_list_dir)

# Load tsx composite index listing
tsx_df = pd.read_csv(glob.glob(os.path.join(tsx_dir, "*"))[0])
name_lst = tsx_df["company"].to_list()
search_lst = [x.replace(".", "").lower() for x in name_lst]

###################################################################################################################

bulk_text = []

url = 'https://www.ic.gc.ca/app/scr/cc/CorporationsCanada/fdrlCrpSrch.html'
# XML dataset 2016?
# https://open.canada.ca/data/en/dataset/0032ce54-c5dd-4b66-99a0-320a7b5e99f2/resource/164ae5ee-8ba2-447e-a443-0ea42a9b10bc

# open browser
driver = webdriver.Chrome()

for every_corp_name in search_lst:
    # load page
    driver.get(url)

    # set to active corp
    selected_dropdown = Select(driver.find_element("id", "corpStatus"))
    selected_dropdown.select_by_value("1")

    # find field
    item = driver.find_element("id", "corpName")

    # put text
    item.send_keys(every_corp_name)

    # find button
    item = driver.find_element("id", "buttonNext")

    # click button
    item.click()

    # find the rows
    all_answers = driver.find_elements(By.CLASS_NAME, "row")

    for each_webelement in all_answers:
        if "Search Results" in each_webelement.text:
            bulk_text.append(each_webelement.text)

    time.sleep(5)

combined_result = []

for each_corp_results in bulk_text:
    if '\n\n' in each_corp_results:  # at least 1 result exists
        strip_hdr = each_corp_results[each_corp_results.index('\n\n')+1:]
        start_pos = []
        end_pos = []
        for result in re.finditer(r".*?\d[.]", strip_hdr):
            start_pos.append(result.start())
            end_pos.append(result.end())

        for i in range(len(start_pos)):
            if i == len(start_pos) - 1:
                combined_result = combined_result + [strip_hdr[end_pos[i]+1:]]
            else:
                combined_result = combined_result + [strip_hdr[end_pos[i]+1:start_pos[i+1]-1]]

combined_dict = {
    "name1": [],
    "name2": [],
    "status": [],
    "business_number": [],
    "corp_number": []
}

for each_corp_result in combined_result:
    list_o_lines = each_corp_result.splitlines()

    if len(list_o_lines) == 5:
        combined_dict["name1"].append(list_o_lines[0])
        combined_dict["name2"].append(list_o_lines[1])
        combined_dict["status"].append(list_o_lines[2].replace("Status:", ""))
        combined_dict["corp_number"].append(list_o_lines[3].replace("Corporation Number:", "").replace("-", ""))
        combined_dict["business_number"].append(list_o_lines[4].replace("Business Number:", ""))
    elif len(list_o_lines) == 4:
        combined_dict["name1"].append(list_o_lines[0])
        combined_dict["name2"].append("")
        combined_dict["status"].append(list_o_lines[1].replace("Status:", ""))
        combined_dict["corp_number"].append(list_o_lines[2].replace("Corporation Number:", "").replace("-", ""))
        combined_dict["business_number"].append(list_o_lines[3].replace("Business Number:", ""))
    else:
        print(f"whoops: failed to capture {each_corp_result}")

df = pd.DataFrame.from_dict(combined_dict)
df.to_csv(os.path.join(save_dir_corp_no, "20221111_corp_no_listing.csv"))

