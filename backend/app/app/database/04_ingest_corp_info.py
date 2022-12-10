from datetime import date
import os
import pathlib
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
data_dir_corp_board = "corp_board"
data_dir_corp_no = "corp_no"
data_dir_tsx = "wiki_tsx"

# Folder creation, directories
curr_dir_name = os.path.dirname(__file__)

absolute_project_path = None
for i in pathlib.Path(curr_dir_name).parents:
    if i.name == project_name:
        absolute_project_path = i.absolute()
        break

board_dir = os.path.join(absolute_project_path, data_dir, data_dir_corp_board)
no_dir = os.path.join(absolute_project_path, data_dir, data_dir_corp_no)
tsx_dir = os.path.join(absolute_project_path, data_dir, data_dir_tsx)

# Load corporation search results
no_csv = glob.glob(no_dir + "/*corp_no_listing.csv")
if len(no_csv) > 1:
    raise RuntimeError("More than one csv detected.")

df = pd.read_csv(no_csv[0])
# 35,THE BANK OF NOVA SCOTIA,, Active, 105195598RC0001, 0950807 has no board?
df.drop([35], inplace=True)
name_1 = df["name1"].to_list()
corp_number = df["corp_number"].to_list()

# Load tsx list for sector/industry
tsx_csv = glob.glob(tsx_dir + "/*tsx.csv")
if len(tsx_csv) > 1:
    raise RuntimeError("More than one csv detected.")

tsx_df = pd.read_csv(tsx_csv[0])
tsx_name = tsx_df["company"].to_list()
tsx_sector = tsx_df["section"].to_list()
tsx_industry = tsx_df["industry"].to_list()

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

for name, number in zip(name_1, corp_number):
    board_csv = glob.glob(board_dir + f"/*{number}.csv")
    board_df = pd.read_csv(board_csv[0])
    first_names = board_df["firstName"].to_list()
    last_names = board_df["lastName"].to_list()

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
        stat = select(Source.id).where(
            Source.data_source == "Innovation, Science and Economic Development Canada, Corporations Canada Search"
        )
        res_source = session.exec(stat).all()

        if len(res_source) > 1:
            raise RuntimeError("Too many sources identified")

        stat = select(OrganizationType.id).where(
            OrganizationType.match_name == "corporation"
        )
        res_org_type = session.exec(stat).all()

        if len(res_org_type) > 1:
            raise RuntimeError("Too many org types identified")

        tsx_sector_match = "nothing found"
        tsx_industry_match = "nothing found"

        for idx, each_tsx_listing in enumerate(tsx_name):
            if create_match_name(name) == create_match_name(each_tsx_listing):
                tsx_sector_match = create_match_name(tsx_sector[idx])
                tsx_industry_match = create_match_name(tsx_industry[idx])
                break

        stat = select(SectorIndustry.id).where(
            SectorIndustry.sector_match_name == tsx_sector_match
        ).where(
            SectorIndustry.industry_match_name == tsx_industry_match
        )
        res_sector = session.exec(stat).all()

        if len(res_sector) == 1:
            ot = Organization(display_name=name,
                              match_name=create_match_name(name),
                              organization_type=res_org_type[0],
                              sector=res_sector[0],
                              source=res_source[0],
                              misc_data={"corporate_number": number})
        else:
            ot = Organization(display_name=name,
                              match_name=create_match_name(name),
                              organization_type=res_org_type[0],
                              source=res_source[0],
                              misc_data={"corporate_number": number})
        session.add(ot)
        session.commit()
        organization_id = ot.id

    else:
        organization_id = res[0]

        # CORPORATE INFO TABLE
        # stat = select(Organization.id).where(
        #     Organization.match_name == create_match_name(name)
        # )
        # res_org = session.exec(stat).all()
        #
        # ot = CorporateInfo(organization=res_org[0],
        #                    corporate_number=number,
        #                    stock_ticker="obs",
        #                    source=res_source[0])
        # session.add(ot)
        # session.commit()

    # PERSON TABLE
    for f, l in zip(first_names, last_names):
        combo = f"{f} {l}"

        # Grab source details for Person and Membership
        stat = select(Source.id).where(
            Source.data_source == "Innovation, Science and Economic Development Canada, Corporations Canada API"
        )
        res_source = session.exec(stat).all()

        if len(res_source) > 1:
            raise RuntimeError("Too many sources identified")

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
            person_id = res_person[0]

        # MEMBERSHIP TABLE
        # Grab source details for Person and Membership
        # TODO: Add remaining logic to get most recent
        stat = select(Source.date_obtained).where(
                Source.data_source == "Innovation, Science and Economic Development Canada, Corporations Canada API"
            )
        res_source_dt = session.exec(stat).all()

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
                                                    start_date=res_source_dt[0],
                                                    end_date=res_source_dt[0],
                                                    source=res_source[0])
            session.add(new_membership)

        else:
            # Existing membership, update end_date
            existing_membership = res_membership[0]
            existing_membership.end_date = res_source_dt[0]
            session.add(existing_membership)
        session.commit()

session.close()

