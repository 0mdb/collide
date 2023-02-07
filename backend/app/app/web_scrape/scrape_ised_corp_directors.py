import requests
import time
import os
import pandas as pd
import glob
from DirectoryHandler import DirectoryHandler
import datetime


def scrape_corp_directors(auth_key):
    """Retrieves board of directors members for each corporation in list file. Uses ISED API and corporate number.
    Do not tamper with sleep timing (usage rate limit).

    Parameters
    ----------
    auth_key: str

    Returns
    -------
    Nothing

    """
    # https://ised-isde.canada.ca/site/corporations-canada/en/data-services#1

    # Preamble, folder locations
    dh_no = DirectoryHandler("corp_no")
    dh_board = DirectoryHandler("corp_board")
    dh_board.load_meta_file()
    dh_board.file_existing()

    save_dir_corp_no = dh_no.path_of_interest
    save_dir_board = dh_board.path_of_interest

    # Add this as a user-key parameter to your API calls to authenticate
    # MAX 60 QUERIES PER MIN

    if auth_key is None:
        raise RuntimeError("Update auth_key")

    # V1
    # url_request = f"https://corporations-ised-isde.api.canada.ca/api/v1/corporations/{business_number}.json?lang=eng"
    # r = requests.get(url_request, headers={"Accept": "application/json", "user-key": f"{auth_key}"})

    # V2
    corp_no = pd.read_csv(glob.glob(os.path.join(save_dir_corp_no, "*listing.csv"))[0])
    corp_listing = corp_no["corp_number"].to_list()
    x = 1

    output_list = []
    for each_corp_number in corp_listing:
        print(f"\t\tLooping: {x} of {len(corp_listing)}")
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
                output_list.append(f"{each_corp_number}.csv")
            except:
                print(f"whoops: failed to retrieve corp no despite code 200, {each_corp_number}")
        else:
            print(f"whoops: failed to retrieve corp no, {each_corp_number}")

        x = x + 1

    # Create meta.csv file
    dh_board.create_meta_file(source_date=datetime.datetime.now(),
                              source_name="Innovation, Science and Economic Development Canada, Corporations Canada API",
                              source_dict={
                                  "url": "https://ised-isde.canada.ca/site/corporations-canada/en/accessing-federal-corporation-json-datasets",
                                  "filenames": output_list})
