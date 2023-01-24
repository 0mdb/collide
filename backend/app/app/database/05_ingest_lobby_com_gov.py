import numpy as np
import pandas as pd
import glob
import common_func as cf
from DirectoryHandler import DirectoryHandler


def insert_gov_lobbycomm_people_orgs_memberships():
    # TODO: Test on fresh db 0/1
    # TODO: Test on populated db 1/1

    # Preamble, folder locations
    dh_comms = DirectoryHandler("lobby_comms")

    dpoh_csv = glob.glob(dh_comms.path_of_interest + "/*DpohExport.csv")
    if len(dpoh_csv) > 1:
        raise RuntimeError("More than one csv detected.")
    df_dpoh = pd.read_csv(dpoh_csv[0])

    prim_csv = glob.glob(dh_comms.path_of_interest + "/*PrimaryExport.csv")
    if len(prim_csv) > 1:
        raise RuntimeError("More than one csv detected.")
    df_prim = pd.read_csv(prim_csv[0])

    df_dpoh = df_dpoh.merge(df_prim, on='COMLOG_ID', how='left')

    first_name_lst = df_dpoh["DPOH_FIRST_NM_PRENOM_TCPD"].to_list()
    last_name_lst = df_dpoh["DPOH_LAST_NM_TCPD"].to_list()
    df_dpoh["INSTITUTION"].replace("Other (Specify)", np.NaN, inplace=True)
    df_dpoh["merged_institution"] = df_dpoh["INSTITUTION"].combine_first(df_dpoh["OTHER_INSTITUTION_AUTRE"])
    org_name_lst = df_dpoh["merged_institution"].to_list()
    date_lst = df_dpoh["COMM_DATE"].to_list()

    session = cf.create_session(debug=True)

    # Grab sources (Monthly Communication Reports)
    dh_comms.load_meta_file()
    comms_source_objs = cf.add_sources(session, [{"data_source": dh_comms.source_name,
                                                  "date_obtained": dh_comms.source_age,
                                                  "misc_data": dh_comms.source_misc}])
    comms_source_id = comms_source_objs[0].id

    # Populate organizations of people in DPOH
    for name, f, l, dt in zip(org_name_lst, first_name_lst, last_name_lst, date_lst):
        # ORGANIZATION TABLE
        # Shows up in INSTITUTION "Other (Specify)"
        party_name_issue_lst = ["Liberal Party of Canada",
                                "Liberal",
                                "Liberal Party of Canada, Official opposition",
                                # "Office of the Leader of the Opposition, Liberal Research Bureau",
                                "Conservative",
                                "NDP",
                                "Parti Libéral"]

        if name in party_name_issue_lst:
            org_type_name = "politicalparty"
        else:
            org_type_name = "government"

        # Insert
        org_objs = cf.add_organizations(session, [{"name": name,
                                                   "org_type_str": org_type_name,
                                                   "org_parent_str": "federalgovernmentofcanada",
                                                   "org_sector_str": "government",
                                                   "org_source_id": comms_source_id,
                                                   "misc": {}}])

        organization_id = org_objs[0].id

        # Populate people table from DPOH names
        combo = f"{f} {l}"

        person_objs = cf.add_people(session, [{"name": combo,
                                               "ppl_source_id": comms_source_id}])
        person_id = person_objs[0].id

        # Populate memberships of people in DPOH
        memberships_objs = cf.add_memberships(session, [{"person_id": person_id,
                                                         "org_id": organization_id,
                                                         "start_date": dt,
                                                         "end_date": dt,
                                                         "source_id": comms_source_id}])

    session.close()
    print("END")

