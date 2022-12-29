import os
import pathlib
from selenium import webdriver
import requests
import time
import pandas as pd

# https://www.ourcommons.ca/members/en/votes?parlSession=44-1

################################################################################################################

parl_sessions = ["38-1",
                 "39-1",
                 "39-2",
                 "40-1",
                 "40-2",
                 "40-3",
                 "41-1",
                 "41-2",
                 "42-1",
                 "43-1",
                 "43-2",
                 "44-1"
                 ]

base_url = r"https://www.ourcommons.ca/members/en/votes/csv?parlSession={}"

################################################################################################################

# Preamble, folder locations
project_name = "app"  # collide\backend\app\app
data_dir = "data"
save_dir_votes = "votes"
save_dir_votes_summary = "summary"

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

################################################################################################################

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
    max_tries = 10
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
    else:
        raise RuntimeWarning(f"couldn't get {csv_link}")

driver.close()

meta_df = pd.DataFrame.from_dict({
    "date_scraped": "2022-12-29T00:00:00+00:00",
    "source_name": "Our Commons Votes Summary",
    "source_url": "https://www.ourcommons.ca/members/en/votes"
})
meta_df.to_csv(os.path.join(save_dir_votes_summary, "meta.csv"))
