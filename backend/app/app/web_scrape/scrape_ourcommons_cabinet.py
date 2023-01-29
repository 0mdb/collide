import requests
import os
import pathlib

project_name = "lobby-force"
data_dir = "data"
save_dir = "data/cabinet_xml"
precedence_start = 77
precedence_end = 96

curr_dir_name = os.path.dirname(__file__)

absolute_project_path = None
for i in pathlib.Path(curr_dir_name).parents:
    if i.name == project_name:
        absolute_project_path = i.absolute()
        break

if not os.path.exists(os.path.join(absolute_project_path, data_dir)):
    os.mkdir(os.path.join(absolute_project_path, data_dir))

if not os.path.exists(os.path.join(absolute_project_path, save_dir)):
    os.mkdir(os.path.join(absolute_project_path, save_dir))

save_dir = os.path.join(absolute_project_path, save_dir)

for p in range(precedence_start, precedence_end + 1):
    url = f"https://www.ourcommons.ca/Members/en/ministries/xml?ministry=29&precedenceReview={p}&province=all&gender=all"

    response = requests.get(url)
    with open(os.path.join(save_dir, f"cabinet_{p}.xml"), 'wb') as file:
        file.write(response.content)
