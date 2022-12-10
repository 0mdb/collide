import datetime
import os
import pathlib
import pandas as pd
from sqlmodel import Session, create_engine, select
from schema_creation.sqlmodel_build import (
    Source
)
import glob
import common_func as cf
from pathlib import Path

# Manually designate sources
# 2022-11-21

# date_obtained: date = Field(sa_column=sa.Column(sa.Date, nullable=False))
# data_source: str
# misc_data: dict = Field(default={}, sa_column=sa.Column(pg.JSONB))

# Preamble, folder locations
project_name = "app"  # collide\backend\app\app
data_dir = "data"
data_dir_ab = "prov_ab"

# Folder creation, directories
curr_dir_name = os.path.dirname(__file__)

absolute_project_path = None
for i in pathlib.Path(curr_dir_name).parents:
    if i.name == project_name:
        absolute_project_path = i.absolute()
        break

file_dir = os.path.join(absolute_project_path, data_dir, data_dir_ab)

session = cf.create_session()

# Insert source for lobbying website
sources = [
    {"date_obtained": datetime.datetime.fromisoformat("2022-12-06T00:00:00+00:00"),
     "data_source": "Alberta Lobby Registry",
     "misc_data": {"filenames": ["lobby_comm_ab.csv"],
                   "url": "https://www.albertalobbyistregistry.ca/"}}
]
src_objs = cf.add_sources(session, sources)

# Insert Government of Alberta as Organization
orgs = [
        {
            "name": "Government of Alberta",
            "org_type_str": "Government",
            "org_parent_str": None,
            "org_sector_str": "Government",
            "org_source_id": src_objs[0].id,
            "misc": {}
        }
    ]
goa_objs = cf.add_organizations(session, orgs)

# Ingest csv
ab_csv = glob.glob(file_dir + "/*lobby_com_ab.csv")

if len(ab_csv) > 1:
    raise RuntimeError("More than one csv detected.")

ab_df = pd.read_csv(ab_csv[0])

# Organization inserts from "Organization"
orgs = []
for each_org in ab_df["Organization"].to_list():
    org_type = cf.match_organization_type(each_org)
    orgs.append(
        {
            "name": each_org,
            "org_type_str": org_type,
            "org_parent_str": None,
            "org_sector_str": None,
            "org_source_id": src_objs[0].id,
            "misc": {}
        }
    )
org_objs = cf.add_organizations(session, orgs)

# Organization inserts from "Client Name"
orgs = []
for each_org in ab_df["Client Name"].to_list():
    org_type = cf.match_organization_type(each_org)
    orgs.append(
        {
            "name": each_org,
            "org_type_str": org_type,
            "org_parent_str": None,
            "org_sector_str": None,
            "org_source_id": src_objs[0].id,
            "misc": {}
        }
    )
client_name_objs = cf.add_organizations(session, orgs)

# Organization inserts from "Government Department Lobbied"
orgs = []
for each_org in ab_df["Government Department Lobbied"].to_list():
    orgs.append(
        {
            "name": each_org,
            "org_type_str": "Government",
            "org_parent_str": "Government of Alberta",
            "org_sector_str": "Government",
            "org_source_id": src_objs[0].id,
            "misc": {}
        }
    )
gov_department_objs = cf.add_organizations(session, orgs)

# Organization inserts from "Prescribed Provincial Entity Lobbied"
orgs = []
for each_org in ab_df["Prescribed Provincial Entity Lobbied"].to_list():
    orgs.append(
        {
            "name": each_org,
            "org_type_str": "Government",
            "org_parent_str": "Government of Alberta",
            "org_sector_str": "Government",
            "org_source_id": src_objs[0].id,
            "misc": {}
        }
    )
gov_entity_objs = cf.add_organizations(session, orgs)

# Person inserts from "Designated Filer"
ppl = []
for each_person in ab_df["Designated Filer"].to_list():
    ppl.append(
        {
            "name": each_person,
            "ppl_source_id": src_objs[0].id,
        }
    )
filer_objs = cf.add_people(session, ppl)

# Person inserts from "Lobbyists"
lobby_objs = []
for each_lobby_lst in ab_df["Lobbyists"].to_list():
    ppl = []
    for each_person in each_lobby_lst.split(","):
        ppl.append(
            {
                "name": each_person,
                "ppl_source_id": src_objs[0].id,
            }
        )
    int_objs = cf.add_people(session, ppl)
lobby_objs.append(int_objs)

# OrganizationMembership inserts between filer and organization + client name
filer_org_memberships = []
filer_client_memberships = []
for each_filer, each_org, each_client, start_str, end_str in zip(filer_objs, org_objs, client_name_objs, ab_df["Filing Date"].to_list(), ab_df["Termination Date"].to_list()):
    filer_org_memberships.append(
        {
            "person_id": each_filer.id,
            "organization_id": each_org.id,
            "start_date": start_str,
            "end_date": end_str,
            "source": src_objs[0].id
        }
    )
    filer_client_memberships.append(
        {
            "person_id": each_filer.id,
            "organization_id": each_client.id,
            "start_date": start_str,
            "end_date": end_str,
            "source": src_objs[0].id
        }
    )
filer_org_membership_objs = cf.add_memberships(session, filer_org_memberships)
filer_client_membership_objs = cf.add_memberships(session, filer_client_memberships)

# TODO: write add_memberships
# TODO: OrganizationMembership inserts between lobbyists and organization/client name
# TODO: CommsTopic inserts from "Subject Matter of Lobbying"
# TODO: CommunicationsP2O (new table?) inserts between filer/lobbyists with departments/entities


session.close()
