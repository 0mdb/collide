import pandas as pd
import glob
from common_func import create_match_name
from DirectoryHandler import DirectoryHandler
import common_func as cf


def insert_corp_people_orgs_memberships(debug_status):
    # Preamble, folder locations
    dh_board = DirectoryHandler("corp_board")
    dh_no = DirectoryHandler("corp_no")
    dh_tsx = DirectoryHandler("wiki_tsx")

    # Load corporation search results
    no_csv = glob.glob(dh_no.path_of_interest + "/*corp_no_listing.csv")
    if len(no_csv) > 1:
        raise RuntimeError("More than one csv detected.")

    df = pd.read_csv(no_csv[0])
    name_1 = df["name1"].to_list()
    corp_number = df["corp_number"].to_list()

    # Load tsx list for sector/industry
    tsx_csv = glob.glob(dh_tsx.path_of_interest + "/*tsx.csv")
    if len(tsx_csv) > 1:
        raise RuntimeError("More than one csv detected.")

    tsx_df = pd.read_csv(tsx_csv[0])
    tsx_name = tsx_df["company"].to_list()
    tsx_sector = tsx_df["section"].to_list()
    tsx_industry = tsx_df["industry"].to_list()

    session = cf.create_session(debug=debug_status)

    # Grab sources (ISED Corp No)
    dh_no.load_meta_file()
    corp_no_source_objs = cf.add_sources(session, [{"data_source": dh_no.source_name,
                                                    "date_obtained": dh_no.source_age,
                                                    "misc_data": dh_no.source_misc}])
    # Insert/Grab source (Corporations Canada API)
    dh_board.load_meta_file()
    corp_board_source_objs = cf.add_sources(session, [{"data_source": dh_board.source_name,
                                                       "date_obtained": dh_board.source_age,
                                                       "misc_data": dh_board.source_misc}])

    for name, number in zip(name_1, corp_number):
        board_csv = glob.glob(dh_board.path_of_interest + f"/*{number}.csv")

        if len(board_csv) == 0:
            print(f"{name} ({number}) does not have a board of directors file")
            # 35,THE BANK OF NOVA SCOTIA,, Active, 105195598RC0001, 0950807 has no board?
            continue

        board_df = pd.read_csv(board_csv[0])
        first_names = board_df["firstName"].to_list()
        last_names = board_df["lastName"].to_list()

        # ORGANIZATION TABLE
        tsx_sector_match = "nothing found"
        tsx_industry_match = "nothing found"

        for idx, each_tsx_listing in enumerate(tsx_name):
            if create_match_name(name) == create_match_name(each_tsx_listing):
                tsx_sector_match = create_match_name(tsx_sector[idx])
                tsx_industry_match = create_match_name(tsx_industry[idx])
                break

        if tsx_sector_match == "nothing found":
            org_dict = {"name": name,
                        "org_type_str": "corporation",
                        "org_source_id": corp_no_source_objs[0].id,
                        "misc": {"corporate_number": number}}

        elif tsx_industry_match == "nothing found":
            org_dict = {"name": name,
                        "org_type_str": "corporation",
                        "org_sector_str": tsx_sector_match,
                        "org_source_id": corp_no_source_objs[0].id,
                        "misc": {"corporate_number": number}}

        else:  # both sector and industry available
            org_dict = {"name": name,
                        "org_type_str": "corporation",
                        "org_sector_str": tsx_sector_match,
                        "org_industry_str": tsx_industry_match,
                        "org_source_id": corp_no_source_objs[0].id,
                        "misc": {"corporate_number": number}}

        corp_org = cf.add_organizations(session, [org_dict])
        organization_id = corp_org[0].id

        # PERSON TABLE
        for f, l in zip(first_names, last_names):
            combo = f"{f} {l}"

            # Insert board member
            person_objs = cf.add_people(session, [{"name": combo,
                                                  "ppl_source_id": corp_board_source_objs[0].id}])
            person_id = person_objs[0].id

            # MEMBERSHIP TABLE
            membership_objs = cf.add_memberships(session, [{"person_id": person_id,
                                                            "org_id": organization_id,
                                                            "start_date": dh_board.source_age,
                                                            "end_date": dh_board.source_age,
                                                            "source_id": corp_board_source_objs[0].id}])

    session.close()
