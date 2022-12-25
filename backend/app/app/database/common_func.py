from datetime import datetime
import os
import pathlib
from sqlmodel import Session, create_engine, select
from schema_creation.sqlmodel_build import (
    Source, Organization, OrganizationType, SectorIndustry, Person, OrganizationMembership,
    FundingPersonPerson, FundingPersonOrg
)
import glob
from pathlib import Path
from parse_injest.utils import create_match_name


def backup_postgres(host, user, passw, db_name, schema_name, pg_dump_command='pg_dump'):
    import subprocess
    import time

    timestr = str(int(time.time()))

    cmd = [pg_dump_command,
           f"-n", schema_name, '-Z', '9', '-f', f"backup_{timestr}.gz", '-d',
           f'postgresql://{user}:{passw}@{host}/{db_name}']

    try:
        popen = subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError:
        print('database backup not made')


def create_session():
    db_host = "localhost"
    db_name = "lq_test"
    db_user = "test_user"
    db_pw = "changethis"
    schema_name = "lf_mockup_2"

    motor = create_engine(
        f"postgresql+psycopg2://{db_user}:{db_pw}@localhost/{db_name}", echo=True
    )

    # backup_postgres(host=db_host,
    #                 user=db_user,
    #                 passw=db_pw,
    #                 db_name=db_name)

    return Session(motor)


def add_sources(session, src_lst):
    src_obj_lst = []
    for each_dict in src_lst:
        # Check if it already exists with same timestamp
        stat = select(Source).where(
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
        stat = select(Person).where(
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
        stat = select(Organization).where(
            Organization.match_name == create_match_name(each_dict.get("name"))
        )
        res = session.exec(stat).all()

        if len(res) == 0:
            # New organization
            stat = select(OrganizationType.id).where(
                OrganizationType.match_name == create_match_name(each_dict.get("org_type_str"))
            )
            res_org_type_id = session.exec(stat).all()

            if len(res_org_type_id) > 1:
                raise RuntimeError("Too many org types identified")

            # Retrieve parent org id from string name if key in dict
            if "org_parent_str" in each_dict.keys():
                stat = select(Organization.id).where(
                    Organization.match_name == create_match_name(each_dict.get("org_parent_str"))
                )
                res_parent_id = session.exec(stat).all()

                if len(res_parent_id) > 1:
                    raise RuntimeError("Too many org parents identified")

            else:
                res_parent_id = [None]

            # Retrieve section id from string name if key in dict
            if "org_sector_str" in each_dict.keys():
                stat = select(SectorIndustry.id).where(
                    SectorIndustry.sector_match_name == create_match_name(each_dict.get("org_sector_str"))
                )
                res_sector_id = session.exec(stat).all()

                if len(res_sector_id) > 1:
                    raise RuntimeError("Too many sectors identified")
            else:
                res_sector_id = [None]

            ot = Organization(display_name=each_dict.get("name"),
                              match_name=create_match_name(each_dict.get("name")),
                              organization_type=res_org_type_id[0],
                              parent_organization=res_parent_id[0],
                              source=each_dict.get("org_source_id"),
                              sector=res_sector_id[0],
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


def add_memberships(session, mem_lst):
    # {
    #     "person_id": int,
    #     "org_id": int,
    #     "start_date": str,
    #     "end_date": str,
    #     "source_id": int,
    # }

    mem_obj_lst = []
    for each_dict in mem_lst:
        # MEMBERSHIP TABLE
        # check if entry unique
        stat = select(OrganizationMembership).where(
            OrganizationMembership.person == each_dict.get("person_id")
        ).where(
            OrganizationMembership.organization == each_dict.get("org_id")
        )
        res_membership = session.exec(stat).all()

        if len(res_membership) == 0:
            # New membership
            new_membership = OrganizationMembership(person=each_dict.get("person_id"),
                                                    organization=each_dict.get("org_id"),
                                                    start_date=datetime.fromisoformat(each_dict.get("start_date")).date(),
                                                    end_date=datetime.fromisoformat(each_dict.get("end_date")).date(),
                                                    source=each_dict.get("source_id"))

            session.add(new_membership)
            session.commit()
            mem_obj_lst.append(new_membership)

        elif len(res_membership) == 1:
            # Existing membership, update end_date
            existing_membership = res_membership[0]

            if existing_membership.end_date < datetime.fromisoformat(each_dict.get("end_date")).date():
                existing_membership.end_date = datetime.fromisoformat(each_dict.get("end_date")).date()
                session.add(existing_membership)
                session.commit()

            mem_obj_lst.append(existing_membership)

        else:
            raise RuntimeError("Too many memberships identified")

    return mem_obj_lst


def add_funding_p2p(session, funding_lst):
    # {
    #     "party_1": int,
    #     "party_2": int,
    #     "amount": int,
    #     "start_date": str,
    #     "end_date": str,
    #     "source_id": int,
    # }

    fund_obj_lst = []
    for each_dict in funding_lst:
        # FundingPersonPerson TABLE
        # check if entry unique (same parties, same amount, same start_date)
        stat = select(FundingPersonPerson).where(
            FundingPersonPerson.party_1 == each_dict.get("party_1")
        ).where(
            FundingPersonPerson.party_2 == each_dict.get("party_2")
        ).where(
            FundingPersonPerson.amount == each_dict.get("amount")
        ).where(
            FundingPersonPerson.start_date == datetime.fromisoformat(each_dict.get("start_date")).date()
        )
        res = session.exec(stat).all()

        if len(res) == 0:
            # New fund transfer
            new = FundingPersonPerson(party_1=each_dict.get("party_1"),
                                      party_2=each_dict.get("party_2"),
                                      amount=each_dict.get("amount"),
                                      start_date=datetime.fromisoformat(each_dict.get("start_date")).date(),
                                      end_date=datetime.fromisoformat(each_dict.get("end_date")).date(),
                                      source=each_dict.get("source_id"))

            session.add(new)
            session.commit()
            fund_obj_lst.append(new)

        elif len(res) == 1:
            # Existing
            existing_membership = res[0]
            fund_obj_lst.append(existing_membership)

        else:
            raise RuntimeError("Too many transfers identified")

    return fund_obj_lst


def add_funding_p2o(session, funding_lst):
    # {
    #     "person": int,
    #     "organization": int,
    #     "amount": int,
    #     "start_date": str,
    #     "end_date": str,
    #     "source_id": int,
    # }

    fund_obj_lst = []
    for each_dict in funding_lst:
        # FundingPersonOrg TABLE
        # check if entry unique (same parties, same amount, same start_date)
        stat = select(FundingPersonOrg).where(
            FundingPersonOrg.person == each_dict.get("person")
        ).where(
            FundingPersonOrg.organization == each_dict.get("organization")
        ).where(
            FundingPersonOrg.amount == each_dict.get("amount")
        ).where(
            FundingPersonOrg.start_date == datetime.fromisoformat(each_dict.get("start_date")).date()
        )
        res = session.exec(stat).all()

        if len(res) == 0:
            # New fund transfer
            new = FundingPersonOrg(person=each_dict.get("person"),
                                   organization=each_dict.get("organization"),
                                   amount=each_dict.get("amount"),
                                   start_date=datetime.fromisoformat(each_dict.get("start_date")).date(),
                                   end_date=datetime.fromisoformat(each_dict.get("end_date")).date(),
                                   source=each_dict.get("source_id"))

            session.add(new)
            session.commit()
            fund_obj_lst.append(new)

        elif len(res) == 1:
            # Existing
            existing_entry = res[0]
            fund_obj_lst.append(existing_entry)

        else:
            raise RuntimeError("Too many transfers identified")

    return fund_obj_lst


def match_organization_type(str_name):
    lc_name = str.lower(str_name)

    if "corporation" in lc_name:
        org_type = "Corporation"
    elif "government" in lc_name:
        org_type = "Government"
    elif "charity" in lc_name:
        org_type = "Charity"
    elif "profession" in lc_name:
        org_type = "Professional Association"
    elif "party" in lc_name:
        org_type = "Political Party"
    else:
        org_type = "Unclassified"

    return org_type


def match_ecanada_organization_type(str_name):
    lc_name = str.lower(str_name)

    if "individual" in lc_name:
        raise AssertionError("Individuals cannot be organizations!!")
    elif "corporation" in lc_name:
        org_type = "Corporation"
    elif "government" in lc_name:
        org_type = "Government"
    elif "trade" in lc_name:
        org_type = "Trade Union"
    elif "business" in lc_name:
        org_type = "Unclassified"
    elif "association" in lc_name:
        org_type = "Unclassified"
    else:
        raise AssertionError("No known org type")

    return org_type
