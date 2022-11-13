import requests
import os
import pathlib
import glob

project_name = "lobby-force"
data_dir = "data"
save_dir = "data/members_xml/member_xml"
link_dir = "data/members_xml/links"

curr_dir_name = os.path.dirname(__file__)

absolute_project_path = None
for i in pathlib.Path(curr_dir_name).parents:
    if i.name == project_name:
        absolute_project_path = i.absolute()
        break

if not os.path.exists(os.path.join(absolute_project_path, save_dir)):
    os.makedirs(os.path.join(absolute_project_path, save_dir), exist_ok=True)

save_dir = os.path.join(absolute_project_path, save_dir)
link_dir = os.path.join(absolute_project_path, link_dir)

if not os.path.isdir(link_dir):
    raise RuntimeError("No directory of links to fetch")

link_file_list = glob.glob(link_dir + "/*.txt")

link_list = []
for file in link_file_list:
    with open(file, 'r') as handle:
        loc_link_list = handle.readlines()

    link_list += loc_link_list

# strip the whitespace out
link_list = [x.strip() for x in link_list]

# convert link_list from a list to a set to get the duplicates out of there
link_list = set(link_list)

for link in link_list:
    # print(link)

    # get the xml link from the basic link
    xml_link = f"{link}/xml"

    # get a filename from the basic link
    fn = os.path.split(link)[1] + ".xml"
    fp = os.path.join(save_dir, fn)

    status_code = None
    max_tries = 10
    cur_try = 0

    while cur_try < max_tries and status_code != requests.codes.ok:
        response = requests.get(xml_link)
        status_code = response.status_code
        cur_try += 1
        print(f"{xml_link}\ttry {cur_try}\tcode {response.status_code}")

    if response.status_code == requests.codes.ok:
        with open(fp, 'wb') as handle:
            handle.write(response.content)
    else:
        raise RuntimeWarning(f"couldn't get {xml_link}")
