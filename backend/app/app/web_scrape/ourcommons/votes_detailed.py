import os
import pathlib
import pandas as pd
from selenium import webdriver
import requests
import time
import glob

################################################################################################################

# https://www.ourcommons.ca/members/en/votes/44/1/244/xml

# Preamble, folder locations
project_name = "app"  # collide\backend\app\app
data_dir = "data"
save_dir_votes = "votes"
save_dir_votes_summary = "summary"
save_dir_votes_detail = "detail"

# Folder creation, directories
curr_dir_name = os.path.dirname(__file__)

absolute_project_path = None
for i in pathlib.Path(curr_dir_name).parents:
    if i.name == project_name:
        absolute_project_path = i.absolute()
        break

if not os.path.exists(os.path.join(absolute_project_path, data_dir)):
    os.mkdir(os.path.join(absolute_project_path, data_dir))
save_dir_votes = os.path.join(absolute_project_path, data_dir, save_dir_votes)

if not os.path.exists(os.path.join(absolute_project_path, data_dir, save_dir_votes, save_dir_votes_summary)):
    os.mkdir(os.path.join(absolute_project_path, data_dir, save_dir_votes, save_dir_votes_summary))
save_dir_votes_summary = os.path.join(absolute_project_path, data_dir, save_dir_votes, save_dir_votes_summary)

if not os.path.exists(os.path.join(absolute_project_path, data_dir, save_dir_votes, save_dir_votes_detail)):
    os.mkdir(os.path.join(absolute_project_path, data_dir, save_dir_votes, save_dir_votes_detail))
save_dir_votes_detail = os.path.join(absolute_project_path, data_dir, save_dir_votes, save_dir_votes_detail)

################################################################################################################

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

################################################################################################################


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
    else:
        raise RuntimeWarning(f"couldn't get {xml_link}")

driver.close()

meta_df = pd.DataFrame.from_dict({
    "date_scraped": "2022-12-29T00:00:00+00:00",
    "source_name": "Our Commons Votes Detailed",
    "source_url": "https://www.ourcommons.ca/members/en/votes"
})
meta_df.to_csv(os.path.join(save_dir_votes_detail, "meta.csv"))
