"""
This script looks for cases where the persons name has been entered in some datasource as LASTNAME FIRSTNAME and looks
for the instance that has the most communications, memberships, fundings associated with it and merges the two entries
"""
from schema_creation.sqlmodel_build import (
    Person,
    OrganizationMembership,
    Communications,
    CommunicationsPersonOrg,
    FundingPersonPerson,
    FundingPersonOrg,
)
from sqlmodel import create_engine, select, Session, col, or_

from parse_injest.utils import create_match_name

actually_do_it = False

db_host = "192.168.0.10"
db_name = "collide"
db_user = "test_user"
db_pw = "change_this"

schema_name = "lf_mockup_2"

engine = create_engine(
    f"postgresql+psycopg2://{db_user}:{db_pw}@{db_host}/{db_name}", echo=False
)
sess = Session(engine)

all_people = sess.exec(select(Person)).all()

for person in all_people:

    # check to make sure the person still exists in the db, since we may have already removed some
    if sess.query(Person).where(Person.id == person.id).count() == 0:
        continue

    dn = person.display_name
    dn_tokens = dn.split(" ")

    # reverse the order of the name
    dn_tokens.reverse()
    reversed_dn = " ".join(dn_tokens)
    reversed_mn = create_match_name(reversed_dn)

    # strangely, this happens; skip it for now
    if reversed_mn == person.match_name:
        continue

    # check for an entry of the reversed name
    sql_query = select(Person).where(Person.match_name == reversed_mn)
    res = sess.exec(sql_query).first()

    if res is not None:
        forward_mem = (
            sess.query(OrganizationMembership)
            .where(OrganizationMembership.person == person.id)
            .count()
        )
        forward_com = (
            sess.query(Communications)
            .where(
                or_(
                    Communications.party_1 == person.id,
                    Communications.party_2 == person.id,
                )
            )
            .count()
        )
        forward_com += (
            sess.query(CommunicationsPersonOrg)
            .where(CommunicationsPersonOrg.person == person.id)
            .count()
        )

        forward_fun = (
            sess.query(FundingPersonOrg)
            .where(FundingPersonOrg.person == person.id)
            .count()
        )
        forward_fun += (
            sess.query(FundingPersonPerson)
            .where(
                or_(
                    FundingPersonPerson.party_1 == person.id,
                    FundingPersonPerson.party_2 == person.id,
                )
            )
            .count()
        )

        backward_mem = (
            sess.query(OrganizationMembership)
            .where(OrganizationMembership.person == res.id)
            .count()
        )
        backward_com = (
            sess.query(Communications)
            .where(
                or_(Communications.party_1 == res.id, Communications.party_2 == res.id)
            )
            .count()
        )
        backward_com += (
            sess.query(CommunicationsPersonOrg)
            .where(CommunicationsPersonOrg.person == res.id)
            .count()
        )

        backward_fun = (
            sess.query(FundingPersonOrg)
            .where(FundingPersonOrg.person == res.id)
            .count()
        )
        backward_fun += (
            sess.query(FundingPersonPerson)
            .where(
                or_(
                    FundingPersonPerson.party_1 == res.id,
                    FundingPersonPerson.party_2 == res.id,
                )
            )
            .count()
        )

        print(f"{dn} is also in the database as {reversed_dn}")
        print(
            f"\tforward mem {forward_mem}, forward com {forward_com}, forward fun {forward_fun}"
        )
        print(
            f"\tbackward mem {backward_mem}, backward com {backward_com}, backward fun {backward_fun}"
        )

        # take the version with the most combined combinations and memberships to keep, and remove the other one
        comb_forward = forward_mem + forward_com + forward_fun
        comb_backward = backward_mem + backward_com + backward_fun

        if comb_forward >= comb_backward:
            print(f"\tkeeping {dn}, getting rid of {reversed_dn}")
            id_to_keep = person.id
            id_to_axe = res.id
        else:
            print(f"\tkeeping {reversed_dn}, getting rid of {dn}")
            id_to_keep = res.id
            id_to_axe = person.id

        sql_query = select(OrganizationMembership).where(
            OrganizationMembership.person == id_to_axe
        )
        memberships_to_update = sess.exec(sql_query).all()
        if len(memberships_to_update) > 0:
            print("\t\tthe following memberships should be updated:")
            for mem in memberships_to_update:
                print(f"\t\t\t{mem}")
                if actually_do_it:
                    mem.person = id_to_keep
                    sess.add(mem)
            if actually_do_it:
                sess.commit()

        sql_query = select(Communications).where(
            or_(
                Communications.party_1 == id_to_axe, Communications.party_2 == id_to_axe
            )
        )
        communications_to_update = sess.exec(sql_query).all()
        if len(communications_to_update) > 0:
            print("\t\tthe following communications should be updated:")
            for com in communications_to_update:
                print(f"\t\t\t{com}")
                if com.party_1 == id_to_axe:
                    com.party_1 = id_to_keep
                elif com.party_2 == id_to_axe:
                    com.party_2 = id_to_keep
                sess.add(com)
            sess.commit()
        sql_query = select(CommunicationsPersonOrg).where(
            CommunicationsPersonOrg.person == id_to_axe
        )
        communications_to_update = sess.exec(sql_query).all()
        if len(communications_to_update) > 0:
            print(
                f"\t\tthe following communications should be updated (person to org):"
            )
            for com in communications_to_update:
                print(f"\t\t\t{com}")
                if actually_do_it:
                    com.person = id_to_keep
                    sess.add(com)
            if actually_do_it:
                sess.commit()

        sql_query = select(FundingPersonOrg).where(FundingPersonOrg.person == id_to_axe)
        fundings_to_update = sess.exec(sql_query).all()
        if len(fundings_to_update) > 0:
            print(f"\t\tthe following fundings should be updated (person-org):")
            for fun in fundings_to_update:
                print(f"\t\t\t{fun}")
                if actually_do_it:
                    fun.person = id_to_keep
                    sess.add(fun)
            if actually_do_it:
                sess.commit()

        sql_query = select(FundingPersonPerson).where(
            or_(
                FundingPersonPerson.party_1 == id_to_axe,
                FundingPersonPerson.party_2 == id_to_axe,
            )
        )
        fundings_to_update = sess.exec(sql_query).all()
        if len(fundings_to_update) > 0:
            print(f"\t\tthe following fundings should be updated (person-person):")
            for fun in fundings_to_update:
                print(f"\t\t\t{fun}")
                if actually_do_it:
                    if fun.party_1 == id_to_axe:
                        fun.party_1 = id_to_keep
                    else:
                        fun.party_2 = id_to_keep
                    sess.add(fun)
            if actually_do_it:
                sess.commit()

        if actually_do_it:
            finally_delete = sess.exec(
                select(Person).where(Person.id == id_to_axe)
            ).first()
            sess.delete(finally_delete)
            sess.commit()

sess.close()
