from datetime import datetime
import os
import pathlib
import numpy as np
import pandas as pd
import glob
from sqlmodel import Session, create_engine, select, engine
from schema_creation.sqlmodel_build import (
    Person, Source, Organization, SectorIndustry, OrganizationType, OrganizationMembership,
    # CorporateInfo,
)
from parse_injest.utils import create_match_name

# Preamble, folder locations
project_name = "app"  # collide\backend\app\app
data_dir = "data"
data_dir_com = "lobby_comms"
data_dir_reg = "lobby_reg"

# Folder creation, directories
curr_dir_name = os.path.dirname(__file__)

absolute_project_path = None
for i in pathlib.Path(curr_dir_name).parents:
    if i.name == project_name:
        absolute_project_path = i.absolute()
        break

com_dir = os.path.join(absolute_project_path, data_dir, data_dir_com)
reg_dir = os.path.join(absolute_project_path, data_dir, data_dir_reg)


dpoh_csv = glob.glob(com_dir + "/*DpohExport.csv")
if len(dpoh_csv) > 1:
    raise RuntimeError("More than one csv detected.")
df_dpoh = pd.read_csv(dpoh_csv[0])

prim_csv = glob.glob(com_dir + "/*PrimaryExport.csv")
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


# Dummy database information
db_host = "localhost"
db_name = "lq_test"
db_user = "test_user"
db_pw = "changethis"
schema_name = "lf_mockup_2"

motor = create_engine(
    f"postgresql+psycopg2://{db_user}:{db_pw}@localhost/{db_name}", echo=False
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

for name, f, l, dt in zip(org_name_lst, first_name_lst, last_name_lst, date_lst):
    # ORGANIZATION TABLE
    # check if entry unique
    stat = select(Organization.id).where(
        Organization.match_name == create_match_name(name)
    )
    res = session.exec(stat).all()

    if len(res) > 1:
        raise RuntimeError("Too many organizations identified")

    if len(res) == 0:
        # New organization

        stat = select(OrganizationType.id).where(
            OrganizationType.match_name == "government"
        )
        res_org_type = session.exec(stat).all()

        if len(res_org_type) > 1:
            raise RuntimeError("Too many org types identified")

        stat = select(Organization.id).where(
            Organization.match_name == "federalgovernmentofcanada"
        )
        res_parent = session.exec(stat).all()

        if len(res_parent) > 1:
            raise RuntimeError("Too many org parents identified")

        stat = select(SectorIndustry.id).where(
            SectorIndustry.sector_match_name == "government"
        )
        res_sector = session.exec(stat).all()

        if len(res_sector) > 1:
            raise RuntimeError("Too many sectors identified")

        # Show up in INSTITUTION "Other (Specify)"
        party_name_issue_lst = ["Liberal Party of Canada",
                                "Liberal",
                                "Liberal Party of Canada, Official opposition",
                                # "Office of the Leader of the Opposition, Liberal Research Bureau",
                                "Conservative",
                                "NDP",
                                "Parti Libéral"]

        if name in party_name_issue_lst:
            stat = select(OrganizationType.id).where(
                OrganizationType.match_name == "politicalparty"
            )
            alt_org_type = session.exec(stat).all()

            if len(alt_org_type) > 1:
                raise RuntimeError("Too many alt org types identified")

            ot = Organization(display_name=name,
                              match_name=create_match_name(name),
                              organization_type=alt_org_type[0],
                              # parent_organization=res_parent[0],
                              source=res_source[0],
                              sector=res_sector[0],
                              misc_data={})
        else:
            ot = Organization(display_name=name,
                              match_name=create_match_name(name),
                              organization_type=res_org_type[0],
                              parent_organization=res_parent[0],
                              source=res_source[0],
                              sector=res_sector[0],
                              misc_data={})
        session.add(ot)
        session.commit()
        organization_id = ot.id

    else:
        # Existing organization
        organization_id = res[0]

######################################################################################
# Populate people table from DPOH names
######################################################################################
    combo = f"{f} {l}"

    # check if entry unique
    stat = select(Person.id).where(
        Person.match_name == create_match_name(combo)
    )
    res_person = session.exec(stat).all()

    if len(res_person) > 1:
        raise RuntimeError("Too many persons identified")

    if len(res_person) == 0:
        # if person entry is new
        ot = Person(display_name=combo,
                    match_name=create_match_name(combo),
                    source=res_source[0])
        session.add(ot)
        session.commit()
        person_id = ot.id
    else:
        # existing person
        person_id = res_person[0]

    ######################################################################################
    # Populate memberships of people in DPOH
    ######################################################################################
    # check if entry unique
    stat = select(OrganizationMembership).where(
        OrganizationMembership.person == person_id
    ).where(
        OrganizationMembership.organization == organization_id
    )
    res_membership = session.exec(stat).all()

    if len(res_membership) > 1:
        raise RuntimeError("Too many memberships identified")

    if len(res_membership) == 0:
        # New membership
        new_membership = OrganizationMembership(person=person_id,
                                                organization=organization_id,
                                                start_date=datetime.fromisoformat(dt),
                                                end_date=datetime.fromisoformat(dt),
                                                source=res_source[0])

        session.add(new_membership)

    else:
        # Existing membership, update end_date
        existing_membership = res_membership[0]

        if existing_membership.end_date < datetime.fromisoformat(dt).date():
            existing_membership.end_date = datetime.fromisoformat(dt)
            session.add(existing_membership)
    session.commit()

session.close()
print("END")


