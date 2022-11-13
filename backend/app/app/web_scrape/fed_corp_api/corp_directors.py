import requests
import time
import os
import pathlib
import pandas as pd
import glob

# https://ised-isde.canada.ca/site/corporations-canada/en/data-services#1

# Preamble, folder locations
project_name = "lobby-force"
data_dir = "data"
save_dir_corp_no = "corp_no"
save_dir_board = "corp_board"
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

if not os.path.exists(os.path.join(absolute_project_path, data_dir, save_dir_board)):
    os.mkdir(os.path.join(absolute_project_path, data_dir, save_dir_board))
save_dir_board = os.path.join(absolute_project_path, data_dir, save_dir_board)

################################################################################################################

# Add this as a user-key parameter to your API calls to authenticate
# MAX 60 QUERIES PER MIN

auth_key = None

if auth_key is None:
    raise RuntimeError("Update auth_key")

# V1
# url_request = f"https://corporations-ised-isde.api.canada.ca/api/v1/corporations/{business_number}.json?lang=eng"
# r = requests.get(url_request, headers={"Accept": "application/json", "user-key": f"{auth_key}"})

# V2
corp_no = pd.read_csv(glob.glob(os.path.join(save_dir_corp_no, "*.csv"))[0])
corp_listing = corp_no["corp_number"].to_list()
x = 1

for each_corp_number in corp_listing:
    print(f"Looping: {x} of {len(corp_listing)}")
    url_request = f"https://corporations-ised-isde.api.canada.ca/api/v2/corporations/{each_corp_number}/directors"

    time.sleep(5)
    r = requests.get(url_request, headers={"Accept": "application/hal+json",
                                           "user-key": f"{auth_key}",
                                           "Accept-Language": "en"})

    if r.status_code == 200:
        try:
            response = r.json()  # returned json
            director_list = response.get("_embedded").get("directors")

            df = pd.DataFrame(director_list)
            df.to_csv(os.path.join(save_dir_board, f"{each_corp_number}.csv"))
        except:
            print(f"whoops: failed to retrieve corp no despite code 200, {each_corp_number}")
    else:
        print(f"whoops: failed to retrieve corp no, {each_corp_number}")

    x = x + 1

print("END")
