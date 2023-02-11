import requests
import os
import datetime
import glob
from DirectoryHandler import DirectoryHandler


def scrape_member_details():
    """Retrieves house of commons member details (name, riding) for each MP in link list.

    Returns
    -------
    Nothing

    """
    dh_member_links = DirectoryHandler("members_xml links")
    dh_member_xml = DirectoryHandler("members_xml member_xml")

    link_dir = dh_member_links.path_of_interest
    save_dir = dh_member_xml.path_of_interest

    dh_member_xml.load_meta_file()
    dh_member_xml.file_existing()
    output_list = []

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
            output_list.append(fn)
        else:
            raise RuntimeWarning(f"couldn't get {xml_link}")

    dh_member_xml.create_meta_file(
        source_date=datetime.datetime.now(),
        source_name="House of Commons Canada",
        source_dict={
            "url": "https://www.ourcommons.ca/members/en",
            "filenames": output_list
        }
    )