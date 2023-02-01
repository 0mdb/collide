import numpy as np
import pandas as pd
import glob
import common_func as cf
from DirectoryHandler import DirectoryHandler


def insert_corp_lobbycomm_people_orgs_memberships(debug_status):
    # Preamble, folder locations
    dh_comms = DirectoryHandler("lobby_comms")
    prim_csv = glob.glob(dh_comms.path_of_interest + "/*PrimaryExport.csv")

    if len(prim_csv) > 1:
        raise RuntimeError("More than one csv detected.")
    df_prim = pd.read_csv(prim_csv[0])

    # Drop rows with EN_CLIENT_ORG_CORP_NM_AN as "*", blank, "null"
    df_prim["EN_CLIENT_ORG_CORP_NM_AN"].replace("", np.NaN, inplace=True)
    df_prim["EN_CLIENT_ORG_CORP_NM_AN"].replace("null", np.NaN, inplace=True)
    df_prim["EN_CLIENT_ORG_CORP_NM_AN"].replace("nan", np.NaN, inplace=True)
    df_prim["EN_CLIENT_ORG_CORP_NM_AN"].replace("*", np.NaN, inplace=True)
    df_prim["merged_client_org"] = df_prim["EN_CLIENT_ORG_CORP_NM_AN"].combine_first(df_prim["FR_CLIENT_ORG_CORP_NM"])
    df_prim.dropna(subset=["merged_client_org"], inplace=True)

    first_name_lst = df_prim["RGSTRNT_1ST_NM_PRENOM_DCLRNT"].to_list()
    last_name_lst = df_prim["RGSTRNT_LAST_NM_DCLRNT"].to_list()
    org_name_lst = df_prim["merged_client_org"].to_list()
    date_lst = df_prim["COMM_DATE"].to_list()

    session = cf.create_session(debug=debug_status)

    # Grab sources (Monthly Communication Reports)
    dh_comms.load_meta_file()
    comms_source_objs = cf.add_sources(session, [{"data_source": dh_comms.source_name,
                                                  "date_obtained": dh_comms.source_age,
                                                  "misc_data": dh_comms.source_misc}])
    comms_source_id = comms_source_objs[0].id

    # Populate organizations of people in RGSTRNT
    for name, f, l, dt in zip(org_name_lst, first_name_lst, last_name_lst, date_lst):
        # ORGANIZATION TABLE
        org_objs = cf.add_organizations(session, [{"name": name,
                                                   "org_type_str": "unclassified",
                                                   "org_source_id": comms_source_id,
                                                   "misc": {}}])
        organization_id = org_objs[0].id

        # Populate people table from RGSTRNT names
        combo = f"{f} {l}"

        ppl_objs = cf.add_people(session, [{"name": combo,
                                            "ppl_source_id": comms_source_id}])

        person_id = ppl_objs[0].id

        # Populate memberships of people in RGSTRNT
        memberships_objs = cf.add_memberships(session, [{"person_id": person_id,
                                                         "org_id": organization_id,
                                                         "start_date": dt,
                                                         "end_date": dt,
                                                         "source_id": comms_source_id}])
    session.close()

