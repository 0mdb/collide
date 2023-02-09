import pandas as pd
import numpy as np
import glob
from DirectoryHandler import DirectoryHandler
import common_func as cf
import datetime


def insert_lobbycomm_communications(debug_status, cutoff_dt):
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

    topic_csv = glob.glob(dh_comms.path_of_interest + "/*SubjectMattersExport.csv")
    if len(topic_csv) > 1:
        raise RuntimeError("More than one csv detected.")
    df_topic = pd.read_csv(topic_csv[0])

    # Combining three files into one
    df_dpoh = df_dpoh.merge(df_prim, on='COMLOG_ID', how='left')
    df_dpoh = df_dpoh.merge(df_topic, on='COMLOG_ID', how='left')
    df_dpoh["SUBJ_MATTER_OBJET"].replace("Other", np.NaN, inplace=True)
    df_dpoh["merged_topic"] = df_dpoh["SUBJ_MATTER_OBJET"].combine_first(df_dpoh["OTHER_SUBJ_MATTER_AUTRE_OBJET"])

    gov_first_name_lst = df_dpoh["DPOH_FIRST_NM_PRENOM_TCPD"].to_list()
    gov_last_name_lst = df_dpoh["DPOH_LAST_NM_TCPD"].to_list()
    corp_first_name_lst = df_dpoh["RGSTRNT_1ST_NM_PRENOM_DCLRNT"].to_list()
    corp_last_name_lst = df_dpoh["RGSTRNT_LAST_NM_DCLRNT"].to_list()
    topic_lst = df_dpoh["merged_topic"].to_list()
    date_lst = df_dpoh["COMM_DATE"].to_list()

    session = cf.create_session(debug=debug_status)

    # Grab sources (Monthly Communication Reports)
    dh_comms.load_meta_file()
    comms_source_objs = cf.add_sources(session, [{"data_source": dh_comms.source_name,
                                                  "date_obtained": dh_comms.source_age,
                                                  "misc_data": dh_comms.source_misc}])
    comms_source_id = comms_source_objs[0].id

    # Populate organizations of people in DPOH
    for gov_f, gov_l, corp_f, corp_l, topic, dt in zip(gov_first_name_lst, gov_last_name_lst,
                                                       corp_first_name_lst, corp_last_name_lst,
                                                       topic_lst, date_lst):
        # if datetime.fromisoformat(dt).date() > date(2022, 6, 14):
        #     continue

        # Gov and corp names should already be populated in table
        gov_party = f"{gov_f} {gov_l}"
        gov_person_id = cf.get_person_id(session, gov_party)

        corp_party = f"{corp_f} {corp_l}"
        corp_person_id = cf.get_person_id(session, corp_party)

        # COMM TABLE
        if datetime.datetime.fromisoformat(dt) > cutoff_dt:
            comms_obj = cf.add_communication(session, [{
                "party_1": gov_person_id,
                "party_2": corp_person_id,
                "com_date": dt,
                "topic": topic,
                "source_id": comms_source_id
            }])

    session.close()
    print("\tcompleted lobbycom comms")
