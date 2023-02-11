from schema_creation.sqlmodel_build import (
    Person,
    OrganizationMembership,
    Communications,
    CommunicationsPersonOrg,
    FundingPersonPerson,
    FundingPersonOrg,
)
from sqlmodel import select, or_
from common_func import create_match_name, create_session
import fix_funcs


def fix_people_005(debug_status):
    """This script looks for cases where the persons name has been entered in some datasource as LASTNAME FIRSTNAME and looks
    for the instance that has the most communications, memberships, fundings associated with it and merges the two entries

    Parameters
    ----------
    debug_status

    Returns
    -------
    Nothing

    """

    actually_do_it = True
    sess = create_session(debug_status)

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

            # Reroute here
            fix_funcs.replace_person(
                old_id=id_to_axe,
                new_id=id_to_keep,
                sess=sess,
                actually_do_it=actually_do_it
            )

    sess.close()
