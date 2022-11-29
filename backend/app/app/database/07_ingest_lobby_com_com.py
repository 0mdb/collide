from datetime import datetime
import os
import pathlib
import pandas as pd
import numpy as np
import glob
from sqlmodel import Session, create_engine, select, engine
from schema_creation.sqlmodel_build import (
    Person, Source, CommsTopic, Communications,
)
from parse_injest.utils import create_match_name

# Preamble, folder locations
project_name = "app"  # collide\backend\app\app
data_dir = "data"
data_dir_com = "lobby_comms"

# Folder creation, directories
curr_dir_name = os.path.dirname(__file__)

absolute_project_path = None
for i in pathlib.Path(curr_dir_name).parents:
    if i.name == project_name:
        absolute_project_path = i.absolute()
        break

com_dir = os.path.join(absolute_project_path, data_dir, data_dir_com)

dpoh_csv = glob.glob(com_dir + "/*DpohExport.csv")
if len(dpoh_csv) > 1:
    raise RuntimeError("More than one csv detected.")
df_dpoh = pd.read_csv(dpoh_csv[0])

prim_csv = glob.glob(com_dir + "/*PrimaryExport.csv")
if len(prim_csv) > 1:
    raise RuntimeError("More than one csv detected.")
df_prim = pd.read_csv(prim_csv[0])

topic_csv = glob.glob(com_dir + "/*SubjectMattersExport.csv")
if len(topic_csv) > 1:
    raise RuntimeError("More than one csv detected.")
df_topic = pd.read_csv(topic_csv[0])

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


# Dummy database information
db_host = "localhost"
db_name = "lq_test"
db_user = "test_user"
db_pw = "changethis"
schema_name = "lf_mockup"

motor = create_engine(
    f"postgresql+psycopg2://{db_user}:{db_pw}@localhost/{db_name}", echo=True
)

session = Session(motor)

# Grab shared data source ID
# TODO: Add remaining logic to get most recent
stat = select(Source.id).where(
    Source.data_source == "Office of the Commissioner of Lobbying of Canada, Monthly Communication Reports"
)
res_source = session.exec(stat).all()

if len(res_source) > 1:
    raise RuntimeError("Too many sources identified")

# TODO: Fix all this duplicated code :| (resolve with member xml .py as well)
######################################################################################
# Populate organizations of people in DPOH
######################################################################################

for gov_f, gov_l, corp_f, corp_l, topic, dt in zip(gov_first_name_lst, gov_last_name_lst,
                                                   corp_first_name_lst, corp_last_name_lst,
                                                   topic_lst, date_lst):

    # Gov and corp names should already be populated in table
    gov_party = f"{gov_f} {gov_l}"
    gov_party = create_match_name(gov_party)

    corp_party = f"{corp_f} {corp_l}"
    corp_party = create_match_name(corp_party)

    # Get party_1 ID
    stat = select(Person.id).where(
        Person.match_name == gov_party
    )
    res_gov = session.exec(stat).all()

    if len(res_gov) > 1:
        raise RuntimeError("Too many people identified")

    # Get party_2 ID
    stat = select(Person.id).where(
        Person.match_name == corp_party
    )
    res_corp = session.exec(stat).all()

    if len(res_corp) > 1:
        raise RuntimeError("Too many people identified")

    if len(res_gov) == 0 or len(res_corp) == 0:
        raise RuntimeError("Run prior step to ensure corp and gov parties are populated in person table")

    # COMM TABLE
    # check if entry unique
    stat = select(Communications.id).where(
        Communications.party_1 == res_gov[0]
    ).where(
        Communications.party_2 == res_corp[0]
    ).where(
        Communications.com_date == datetime.fromisoformat(dt).date()
    )
    res_1 = session.exec(stat).all()

    if len(res_1) > 1:
        raise RuntimeError("Too many communications identified")

    stat = select(Communications.id).where(
        Communications.party_1 == res_corp[0]
    ).where(
        Communications.party_2 == res_gov[0]
    ).where(
        Communications.com_date == datetime.fromisoformat(dt).date()
    )
    res_2 = session.exec(stat).all()

    if len(res_2) > 1:
        raise RuntimeError("Too many communications identified")

    if len(res_1) == 0 and len(res_2) == 0:
        # New communication
        # Get topic ID
        stat = select(CommsTopic.id).where(
            CommsTopic.match_name == create_match_name(topic)
        )
        res_topic = session.exec(stat).all()

        if len(res_topic) > 1:
            raise RuntimeError("Too many topics identified")

        print("TOPIC:" + topic)

        ot = Communications(party_1=res_gov[0],
                            party_2=res_corp[0],
                            com_date=datetime.fromisoformat(dt),
                            topic=res_topic[0],
                            source=res_source[0]
                            )

        session.add(ot)
        session.commit()
