import requests
import os
from DirectoryHandler import DirectoryHandler
import datetime


def scrape_cabinet_members(precedence_start, precedence_end):
    """Retrieves members of cabinet for each specified precedence (new precedence = cabinet shuffle).
    Only includes Trudeau government at the moment.

    Parameters
    ----------
    precedence_start: int
    precedence_end: int

    Returns
    -------
    Nothing

    """
    dh_cabinet = DirectoryHandler("cabinet_xml")
    dh_cabinet.load_meta_file()
    dh_cabinet.file_existing()
    output_list = []
    save_dir = dh_cabinet.path_of_interest

    for p in range(precedence_start, precedence_end + 1):
        url = f"https://www.ourcommons.ca/Members/en/ministries/xml?ministry=29&precedenceReview={p}&province=all&gender=all"

        response = requests.get(url)
        with open(os.path.join(save_dir, f"cabinet_{p}.xml"), 'wb') as file:
            file.write(response.content)
        output_list.append(f"cabinet_{p}.xml")

    dh_cabinet.create_meta_file(
        source_date=datetime.datetime.now(),
        source_name="House of Commons Canada",
        source_dict={
            "url": "https://www.ourcommons.ca/members/en",
            "filenames": output_list
        }
    )
