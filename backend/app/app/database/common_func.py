from datetime import datetime
from sqlmodel import Session, create_engine, select
from schema_creation.sqlmodel_build import (
    Source, Organization, OrganizationType, SectorIndustry, Person, OrganizationMembership,
    FundingPersonPerson, FundingPersonOrg, Funding,
    Bill, Vote, VoteIndividual, BillDiff, LegStage
)
from parse_injest.utils import create_match_name
import numpy as np
import gzip


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


def create_session(debug=True, **kwargs):
    if debug:
        db_host = "localhost"
        db_name = "lq_test"
        db_user = "test_user"
        db_pw = "changethis"
        # schema_name = "lf_mockup_2"
    else:
        db_host = "192.168.0.10"
        db_name = "collide"
        db_user = "test_user"
        db_pw = "change_this"
        # schema_name = "lf_mockup_2"

    db_host = kwargs.pop('db_host', db_host)
    db_name = kwargs.pop('db_name', db_name)
    db_user = kwargs.pop('db_user', db_user)
    db_pw = kwargs.pop('db_pw', db_pw)

    motor = create_engine(
        f"postgresql+psycopg2://{db_user}:{db_pw}@{db_host}/{db_name}", echo=False
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

            if existing_membership.start_date > datetime.fromisoformat(each_dict.get("start_date")).date():
                existing_membership.start_date = datetime.fromisoformat(each_dict.get("start_date")).date()
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


def add_funding_o2o(session, funding_lst):
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
        # Funding TABLE
        # check if entry unique (same parties, same amount, same start_date)
        stat = select(Funding).where(
            Funding.party_1 == each_dict.get("party_1")
        ).where(
            Funding.party_2 == each_dict.get("party_2")  # recipient
        ).where(
            Funding.amount == each_dict.get("amount")
        ).where(
            Funding.start_date == datetime.fromisoformat(each_dict.get("start_date")).date()
        )
        res = session.exec(stat).all()

        if len(res) == 0:
            # New fund transfer
            new = Funding(party_1=each_dict.get("party_1"),
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


def add_bills(session, bill_lst):
    bill_obj_lst = []
    for each_dict in bill_lst:
        # Check if it already exists with same match_name
        parl = each_dict.get("parliament")
        parl_sess = each_dict.get("parliament_session")
        name = each_dict.get("bill_name")
        bill_match_name = f"{parl}_{parl_sess}_{name.lower()}"  # parl_session_name
        stat = select(Bill).where(
            Bill.match_name == bill_match_name
        )
        res = session.exec(stat).all()

        # Date handling
        if each_dict.get("first_house_read_date") is not None:
            first_house_read_dt = each_dict.get("first_house_read_date").split("T")[0]
            first_house_read_dt = datetime.fromisoformat(first_house_read_dt).date()
        else:
            first_house_read_dt = None

        if each_dict.get("second_house_read_date") is not None:
            second_house_read_dt = each_dict.get("second_house_read_date").split("T")[0]
            second_house_read_dt = datetime.fromisoformat(second_house_read_dt).date()
        else:
            second_house_read_dt = None

        if each_dict.get("third_house_read_date") is not None:
            third_house_read_dt = each_dict.get("third_house_read_date").split("T")[0]
            third_house_read_dt = datetime.fromisoformat(third_house_read_dt).date()
        else:
            third_house_read_dt = None

        if each_dict.get("first_senate_read_date") is not None:
            first_sen_read_dt = each_dict.get("first_senate_read_date").split("T")[0]
            first_sen_read_dt = datetime.fromisoformat(first_sen_read_dt).date()
        else:
            first_sen_read_dt = None

        if each_dict.get("second_senate_read_date") is not None:
            second_sen_read_dt = each_dict.get("second_senate_read_date").split("T")[0]
            second_sen_read_dt = datetime.fromisoformat(second_sen_read_dt).date()
        else:
            second_sen_read_dt = None

        if each_dict.get("third_senate_read_date") is not None:
            third_sen_read_dt = each_dict.get("third_senate_read_date").split("T")[0]
            third_sen_read_dt = datetime.fromisoformat(third_sen_read_dt).date()
        else:
            third_sen_read_dt = None

        if each_dict.get("royal_assent_date") is not None:
            royal_assent_dt = each_dict.get("royal_assent_date").split("T")[0]
            royal_assent_dt = datetime.fromisoformat(royal_assent_dt).date()
        else:
            royal_assent_dt = None

        if len(res) == 0:
            # New entry

            ot = Bill(bill_name=each_dict.get("bill_name"),
                      parliament=each_dict.get("parliament"),
                      parliament_session=each_dict.get("parliament_session"),
                      match_name=bill_match_name,
                      description=each_dict.get("description"),
                      is_house_bill=each_dict.get("is_house_bill"),
                      is_senate_bill=each_dict.get("is_senate_bill"),

                      first_house_read_date=first_house_read_dt,
                      second_house_read_date=second_house_read_dt,
                      third_house_read_date=third_house_read_dt,
                      first_senate_read_date=first_sen_read_dt,
                      second_senate_read_date=second_sen_read_dt,
                      third_senate_read_date=third_sen_read_dt,
                      royal_assent_date=royal_assent_dt,

                      is_read_first_house=(False if first_house_read_dt is None else True),
                      is_read_second_house=(False if second_house_read_dt is None else True),
                      is_read_third_house=(False if third_house_read_dt is None else True),
                      is_read_first_senate=(False if first_sen_read_dt is None else True),
                      is_read_second_senate=(False if second_sen_read_dt is None else True),
                      is_read_third_senate=(False if third_sen_read_dt is None else True),
                      is_passed_royal_assent=(False if royal_assent_dt is None else True),

                      source=each_dict.get("source_id"))
            session.add(ot)
            session.commit()
            bill_obj_lst.append(ot)
        elif len(res) == 1:
            # Existing entry
            # Update read_date and bools
            existing_bill = res[0]

            if not existing_bill.is_read_first_house and first_house_read_dt is not None:
                # Update
                existing_bill.is_read_first_house = True
                existing_bill.first_house_read_date = first_house_read_dt

            if not existing_bill.is_read_second_house and second_house_read_dt is not None:
                # Update
                existing_bill.is_read_second_house = True
                existing_bill.second_house_read_date = second_house_read_dt

            if not existing_bill.is_read_third_house and third_house_read_dt is not None:
                # Update
                existing_bill.is_read_third_house = True
                existing_bill.third_house_read_date = third_house_read_dt

            if not existing_bill.is_read_first_senate and first_sen_read_dt is not None:
                # Update
                existing_bill.is_read_first_senate = True
                existing_bill.first_senate_read_date = first_sen_read_dt

            if not existing_bill.is_read_second_senate and second_sen_read_dt is not None:
                # Update
                existing_bill.is_read_second_senate = True
                existing_bill.second_senate_read_date = second_sen_read_dt

            if not existing_bill.is_read_third_senate and third_sen_read_dt is not None:
                # Update
                existing_bill.is_read_third_senate = True
                existing_bill.third_senate_read_date = third_sen_read_dt

            if not existing_bill.is_passed_royal_assent and royal_assent_dt is not None:
                # Update
                existing_bill.is_passed_royal_assent = True
                existing_bill.royal_assent_date = royal_assent_dt

            session.add(existing_bill)
            session.commit()

            bill_obj_lst.append(existing_bill)
        else:
            raise RuntimeError("Non unique bill detected")
    return bill_obj_lst


def add_votes(session, vote_lst):
    """
    {
        "parliament": parl[idx],
        "parliament_session": parl_session[idx],
        "date_held": dates[idx],
        "vote_number": each_vote_no,
        "description": desc[idx],
        "yeas": yeas[idx],
        "nays": nays[idx],
        "paired": pairs[idx],
        "result": vote_res[idx],
        "bill_name": bill_no[idx],
        "source_id": summary_src_obj.id
    }
    """
    vote_obj_lst = []
    for each_dict in vote_lst:
        # Check if it already exists with same match_name
        parl = each_dict.get("parliament")
        parl_sess = each_dict.get("parliament_session")
        vote_no = each_dict.get("vote_number")
        vote_match_name = f"{parl}_{parl_sess}_{vote_no}"  # parl_session_voteno

        stat = select(Vote).where(
            Vote.match_name == vote_match_name
        )
        res = session.exec(stat).all()

        # Date handling
        date_dt = each_dict.get("date_held").split()[0]
        date_dt = datetime.fromisoformat(date_dt).date()

        if len(res) == 0:
            # New entry
            if each_dict.get("bill_name") is np.nan:
                bill_id = None
            else:
                bill_name = each_dict.get("bill_name").lower()
                bill_match_name = f"{parl}_{parl_sess}_{bill_name}"

                stat_bill = select(Bill).where(
                    Bill.match_name == bill_match_name
                )
                res_bill = session.exec(stat_bill).all()

                if len(res_bill) == 0 or len(res_bill) > 1:
                    raise AssertionError(f"Bill does not exist or is not unique ({bill_match_name})")

                bill_id = res_bill[0].id

            ot = Vote(parliament=parl,
                      parliament_session=parl_sess,
                      date_held=date_dt,
                      vote_number=vote_no,
                      match_name=vote_match_name,
                      description=each_dict.get("description"),
                      yeas=each_dict.get("yeas"),
                      nays=each_dict.get("nays"),
                      paired=each_dict.get("paired"),
                      result=each_dict.get("result"),
                      bill=bill_id,
                      source=each_dict.get("source_id"))

            session.add(ot)
            session.commit()
            vote_obj_lst.append(ot)
        elif len(res) == 1:
            # Existing entry
            existing_vote = res[0]
            vote_obj_lst.append(existing_vote)
        else:
            raise RuntimeError("Non unique vote detected")
    return vote_obj_lst


def add_individual_votes(session, ind_vote_lst):
    """
        {"parliament": parl[idx],
        "parliament_session": parl_session[idx],
        "vote_no": vote_no[idx],
        "first_name": first_name[idx],
        "last_name": last_name[idx],
        "yes_bool": yes_bool[idx],
        "no_bool": no_bool[idx],
        "pair_bool": pair_bool[idx],
        "source_id": detail_src_obj.id}
    """
    # Check if it already exists with same vote.id and person.id
    stat = select(VoteIndividual)
    all_vote_res = session.exec(stat).all()
    lst_o_tuples = []
    for each_all_vote_res_entry in all_vote_res:
        new_tuple = (each_all_vote_res_entry.person, each_all_vote_res_entry.vote)
        lst_o_tuples.append(new_tuple)

    set_o_tuples = set(lst_o_tuples)

    if len(set_o_tuples) != len(lst_o_tuples):
        raise RuntimeError("Non unique individual vote detected in table")

    ind_vote_obj_lst = []
    for jdx, each_dict in enumerate(ind_vote_lst):
        print(f"IndVotes loop: {jdx} of {len(ind_vote_lst)}")
        # Retrieve vote.id and person.id
        vote_match_name = str(each_dict.get("parliament")) + "_" + str(each_dict.get("parliament_session")) + "_" + str(each_dict.get("vote_no"))
        person_display_name = each_dict.get("first_name") + " " + each_dict.get("last_name")
        person_match_name = create_match_name(person_display_name)

        stat = select(Vote).where(
            Vote.match_name == vote_match_name
        )
        vote_res = session.exec(stat).all()

        if len(vote_res) == 0 or len(vote_res) > 1:
            raise AssertionError(f"Vote does not exist or is not unique ({vote_match_name})")

        stat = select(Person).where(
            Person.match_name == person_match_name
        )
        person_res = session.exec(stat).all()

        if len(person_res) == 0 or len(person_res) > 1:
            raise AssertionError(f"Person does not exist or is not unique ({person_match_name})")

        new_tuple = (person_res[0].id, vote_res[0].id)
        if new_tuple not in set_o_tuples:
            # New entry
            set_o_tuples.add(new_tuple)
            ot = VoteIndividual(vote=vote_res[0].id,
                                person=person_res[0].id,
                                is_yea=each_dict.get("yes_bool"),
                                is_nay=each_dict.get("no_bool"),
                                is_paired=each_dict.get("pair_bool"),
                                source=each_dict.get("source_id"))

            session.add(ot)
            session.commit()
            ind_vote_obj_lst.append(-1)
        else:
            # Existing entry
            # existing_vote = ind_vote_res[0]
            ind_vote_obj_lst.append(-1)
    return ind_vote_obj_lst


def add_individual_votes_single(inputs):
    """
        {"parliament": parl[idx],
        "parliament_session": parl_session[idx],
        "vote_no": vote_no[idx],
        "first_name": first_name[idx],
        "last_name": last_name[idx],
        "yes_bool": yes_bool[idx],
        "no_bool": no_bool[idx],
        "pair_bool": pair_bool[idx],
        "source_id": detail_src_obj.id}
    """
    ind_vote_obj_lst = []

    session_dict, each_dict = inputs


    loc_sess = create_session(**session_dict)

    # Retrieve vote.id and person.id
    vote_match_name = str(each_dict.get("parliament")) + "_" + str(each_dict.get("parliament_session")) + "_" + str(each_dict.get("vote_no"))
    person_display_name = each_dict.get("first_name") + " " + each_dict.get("last_name")
    person_match_name = create_match_name(person_display_name)

    stat = select(Vote).where(
        Vote.match_name == vote_match_name
    )
    vote_res = loc_sess.exec(stat).all()

    if len(vote_res) == 0 or len(vote_res) > 1:
        raise AssertionError(f"Vote does not exist or is not unique ({vote_match_name})")

    stat = select(Person).where(
        Person.match_name == person_match_name
    )
    person_res = loc_sess.exec(stat).all()

    if len(person_res) == 0 or len(person_res) > 1:
        raise AssertionError(f"Person does not exist or is not unique ({person_match_name})")

    # Check if it already exists with same vote.id and person.id
    stat = select(VoteIndividual).where(
        VoteIndividual.person == person_res[0].id
    ).where(
        VoteIndividual.vote == vote_res[0].id
    )
    ind_vote_res = loc_sess.exec(stat).all()

    if len(ind_vote_res) == 0:
        # New entry
        ot = VoteIndividual(vote=vote_res[0].id,
                            person=person_res[0].id,
                            is_yea=each_dict.get("yes_bool"),
                            is_nay=each_dict.get("no_bool"),
                            is_paired=each_dict.get("pair_bool"),
                            source=each_dict.get("source_id"))

        loc_sess.add(ot)
        loc_sess.commit()
        ind_vote_obj_lst.append(ot)
    elif len(ind_vote_res) == 1:
        # Existing entry
        existing_vote = ind_vote_res[0]
        ind_vote_obj_lst.append(existing_vote)
    else:
        raise RuntimeError("Non unique individual vote detected")

    loc_sess.close()

    return ind_vote_obj_lst


def add_diffs(session, diffs_lst):
    """
    {
        "bill_id": each_bill_id,
        "stage_1_id": start_id,
        "stage_2_id": end_id,
        "txt_diff": compressed_html,
    }
    """
    diff_obj_lst = []
    for each_dict in diffs_lst:
        # Check if it already exists with same bill, stage 1 and 2
        bill_id = each_dict.get("bill_id")
        stage_1_id = each_dict.get("stage_1_id")
        stage_2_id = each_dict.get("stage_2_id")

        stat = select(BillDiff).where(
            BillDiff.bill == bill_id
        ).where(
            BillDiff.stage_1 == stage_1_id
        ).where(
            BillDiff.stage_2 == stage_2_id
        )
        res = session.exec(stat).all()

        if len(res) == 0:
            # New entry
            ot = BillDiff(bill=bill_id,
                          stage_1=stage_1_id,
                          stage_2=stage_2_id,
                          txt_diff=each_dict.get("txt_diff"))

            session.add(ot)
            session.commit()
            diff_obj_lst.append(ot)
        elif len(res) == 1:
            # Existing entry
            existing_billdiif = res[0]
            diff_obj_lst.append(existing_billdiif)
        else:
            raise RuntimeError("Non unique billdiff detected")
    return diff_obj_lst


def decode_billdiff(bill_id, stage_1_id, stage_2_id):
    session = create_session()

    stat = select(BillDiff).where(
        BillDiff.bill == bill_id
    ).where(
        BillDiff.stage_1 == stage_1_id
    ).where(
        BillDiff.stage_2 == stage_2_id
    )
    res = session.exec(stat).all()

    if len(res) != 1:
        raise AssertionError("wrong")

    plain_string_again = gzip.decompress(res[0].txt_diff).decode('utf-8')

    with open(f"decoded_table.html", "w") as text_file:
        text_file.write(plain_string_again)


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


def match_ecanada_contrib_org_type(str_name):
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
        raise AssertionError("No known contributor org type")

    return org_type


def match_ecanada_recip_org_type(str_name):
    lc_name = str.lower(str_name)

    if "parties" in lc_name:
        org_type = "Political Party"
    elif "association" in lc_name:
        org_type = "Unclassified"
    else:
        raise AssertionError("No known recipient org type")

    return org_type
