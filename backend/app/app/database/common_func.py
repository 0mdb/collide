import datetime
import os
import pathlib
from sqlmodel import Session, create_engine, select
from schema_creation.sqlmodel_build import (
    Source, Organization, OrganizationType, SectorIndustry, Person
)
import glob
from pathlib import Path
from parse_injest.utils import create_match_name


def create_session():
    db_host = "localhost"
    db_name = "lq_test"
    db_user = "test_user"
    db_pw = "changethis"
    schema_name = "lf_mockup_2"

    motor = create_engine(
        f"postgresql+psycopg2://{db_user}:{db_pw}@localhost/{db_name}", echo=True
    )

    return Session(motor)


def add_sources(session, src_lst):
    src_obj_lst = []
    for each_dict in src_lst:
        # Check if it already exists with same timestamp
        stat = select(Source.id).where(
            Source.data_source == each_dict.get("data_source")
        ).where(
            Source.date_obtained == each_dict.get("date_obtained"))
        res = session.exec(stat).all()

        if len(res) == 0:
            # New entry
            ot = Source(data_source=each_dict.get("data_source"),
                        date_obtained=each_dict.get("date_obtained"),
                        misc_data=each_dict.get("misc_data"))
            session.add(ot)
            session.commit()
            src_obj_lst.append(ot)
        elif len(res) == 1:
            # Existing entry
            src_obj_lst.append(res[0])
        else:
            raise RuntimeError("Non unique source detected")
    return src_obj_lst


def add_people(session, ppl_lst):
    ppl_obj_lst = []
    for each_dict in ppl_lst:
        # Check if it already exists with same match_name
        stat = select(Person.id).where(
            Person.match_name == create_match_name(each_dict.get("name"))
        )
        res = session.exec(stat).all()

        if len(res) == 0:
            # New entry
            ot = Person(display_name=each_dict.get("name"),
                        match_name=create_match_name(each_dict.get("name")),
                        source=each_dict.get("ppl_source_id"))
            session.add(ot)
            session.commit()
            ppl_obj_lst.append(ot)
        elif len(res) == 1:
            # Existing entry
            ppl_obj_lst.append(res[0])
        else:
            raise RuntimeError("Non unique person detected")
    return ppl_obj_lst


def add_organizations(session, org_lst):
    # {
    #     "name": "abc",
    #     "org_type_str": "abc",
    #     "org_parent_str": "abc",
    #     "org_sector_str": "abc",
    #     "org_source_id": int,
    #     "misc": {}
    # }

    org_obj_lst = []
    for each_dict in org_lst:
        # ORGANIZATION TABLE
        # check if entry unique
        stat = select(Organization.id).where(
            Organization.match_name == create_match_name(each_dict.get("name"))
        )
        res = session.exec(stat).all()

        if len(res) == 0:
            # New organization
            stat = select(OrganizationType.id).where(
                OrganizationType.match_name == create_match_name(each_dict.get("org_type_str"))
            )
            res_org_type = session.exec(stat).all()

            if len(res_org_type) > 1:
                raise RuntimeError("Too many org types identified")

            stat = select(Organization.id).where(
                Organization.match_name == create_match_name(each_dict.get("org_parent_str"))
            )
            res_parent = session.exec(stat).all()

            if len(res_parent) > 1:
                raise RuntimeError("Too many org parents identified")

            stat = select(SectorIndustry.id).where(
                SectorIndustry.sector_match_name == create_match_name(each_dict.get("org_sector_str"))
            )
            res_sector = session.exec(stat).all()

            if len(res_sector) > 1:
                raise RuntimeError("Too many sectors identified")

            ot = Organization(display_name=each_dict.get("name"),
                              match_name=create_match_name(each_dict.get("name")),
                              organization_type=res_org_type[0],
                              parent_organization=res_parent[0],
                              source=each_dict.get("org_source_id"),
                              sector=res_sector[0],
                              misc_data={})
            session.add(ot)
            session.commit()
            org_obj_lst.append(ot)
        elif len(res) == 1:
            # Existing entry
            org_obj_lst.append(res[0])
        else:
            raise RuntimeError("Too many organizations identified")
    return org_obj_lst


def match_organization_type(str_name):
    lc_name = str.lower(str_name)

    if "corporation" in lc_name:
        org_type = "Corporation"
    elif "government" in lc_name:
        org_type = "Goverment"
    elif "charity" in lc_name:
        org_type = "Charity"
    elif "profession" in lc_name:
        org_type = "Professional Association"
    elif "party" in lc_name:
        org_type = "Political Party"
    else:
        org_type = "Unclassified"

    return org_type