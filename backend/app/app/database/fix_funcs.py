from schema_creation.sqlmodel_build import (
    OrganizationMembership,
    Organization,
    Communications,
    CommunicationsOrgOrg,
    CommunicationsPersonOrg,
    OrganizationType,
    Funding,
    Person,
    FundingPersonPerson,
    FundingPersonOrg,
    VoteIndividual,
)

from sqlmodel import select
from sqlmodel import or_
import common_func as cf


def return_preferred_party_name(match_name_in_question):
    bloc_name_set = {"blocquebecois", "blocquebecoiscaucus"}
    ndp_name_set = {"newdemocraticparty", "ndpcaucus", "ndp"}
    liberal_name_set = {
        "liberalpartyofcanada",
        "liberalcaucus",
        "liberal",
        "partiliberal",
        "liberalpartyofcanadaofficialopposition",
    }
    con_name_set = {"conservativepartyofcanada", "conservative", "conservativecaucus"}
    ind_name_set = {"independent", "independentcaucus"}
    green_name_set = {"greenpartyofcanada", "greenpartycaucus"}

    if match_name_in_question in bloc_name_set:
        return "blocquebecois"

    if match_name_in_question in ndp_name_set:
        return "newdemocraticparty"

    if match_name_in_question in liberal_name_set:
        return "liberalpartyofcanada"

    if match_name_in_question in con_name_set:
        return "conservativepartyofcanada"

    if match_name_in_question in ind_name_set:
        return "independent"

    if match_name_in_question in green_name_set:
        return "greenpartyofcanada"

    return -1


def replace_organization(old_id, new_id, sess, actually_do_it):
    # old_id is the one that is going to be removed

    # update communicationsorgorg party_1 links
    sql_query = select(CommunicationsOrgOrg).where(
        CommunicationsOrgOrg.party_1 == old_id
    )
    res = sess.exec(sql_query).all()

    for each_commsorgorg_p1 in res:
        each_commsorgorg_p1.party_1 = new_id

        if actually_do_it:
            sess.add(each_commsorgorg_p1)
            sess.commit()

    # update communicationsorgorg party_2 links
    sql_query = select(CommunicationsOrgOrg).where(
        CommunicationsOrgOrg.party_2 == old_id
    )
    res = sess.exec(sql_query).all()

    for each_commsorgorg_p2 in res:
        each_commsorgorg_p2.party_2 = new_id

        if actually_do_it:
            sess.add(each_commsorgorg_p2)
            sess.commit()

    # update communicationspersonorg links
    sql_query = select(CommunicationsPersonOrg).where(
        CommunicationsPersonOrg.organization == old_id
    )
    res = sess.exec(sql_query).all()

    for each_commspersonorg in res:
        each_commspersonorg.organization = new_id

        if actually_do_it:
            sess.add(each_commspersonorg)
            sess.commit()

    # update fundingpersonorg links
    sql_query = select(FundingPersonOrg).where(FundingPersonOrg.organization == old_id)
    res = sess.exec(sql_query).all()

    for each_fundingpersonorg in res:
        each_fundingpersonorg.organization = new_id

        if actually_do_it:
            sess.add(each_fundingpersonorg)
            sess.commit()

    # update funding party_1 links
    sql_query = select(Funding).where(Funding.party_1 == old_id)
    res = sess.exec(sql_query).all()

    for each_funding_p1 in res:
        each_funding_p1.party_1 = new_id

        if actually_do_it:
            sess.add(each_funding_p1)
            sess.commit()

    # update funding party_2 links
    sql_query = select(Funding).where(Funding.party_2 == old_id)
    res = sess.exec(sql_query).all()

    for each_funding_p2 in res:
        each_funding_p2.party_2 = new_id

        if actually_do_it:
            sess.add(each_funding_p2)
            sess.commit()

    # update organizationmembership links
    sql_query = select(OrganizationMembership).where(
        OrganizationMembership.organization == old_id
    )
    res = sess.exec(sql_query).all()

    for each_membership in res:
        each_membership.organization = new_id

        if actually_do_it:
            sess.add(each_membership)
            sess.commit()

    # update organization (parent_organization) links
    sql_query = select(Organization).where(Organization.parent_organization == old_id)
    res = sess.exec(sql_query).all()

    for each_parent_org in res:
        each_parent_org.parent_organization = new_id

        if actually_do_it:
            sess.add(each_parent_org)
            sess.commit()

    # delete organization entry
    if actually_do_it:
        final_moments = sess.exec(
            select(Organization).where(Organization.id == old_id)
        ).first()
        sess.delete(final_moments)
        sess.commit()


def replace_person(old_id, new_id, sess, actually_do_it):
    # old_id is the one that is going to be removed

    # MEMBERSHIP DEPENDENCIES
    sql_query = select(OrganizationMembership).where(
        OrganizationMembership.person == old_id
    )
    memberships_to_update = sess.exec(sql_query).all()
    if len(memberships_to_update) > 0:
        print(
            "\t\t\t\tthe following memberships should be updated:"
        )
        for mem in memberships_to_update:
            print(f"\t\t\t\t\t{mem}")
            if actually_do_it:
                mem.person = new_id
                sess.add(mem)
        if actually_do_it:
            sess.commit()

    # COMMUNICATIONS DEPENDENCIES
    sql_query = select(Communications).where(
        or_(
            Communications.party_1 == old_id,
            Communications.party_2 == old_id,
        )
    )
    communications_to_update = sess.exec(sql_query).all()
    if len(communications_to_update) > 0:
        print(
            "\t\t\t\tthe following communications should be updated:"
        )
        for com in communications_to_update:
            print(f"\t\t\t\t\t{com}")
            if actually_do_it:
                if com.party_1 == old_id:
                    com.party_1 = new_id
                elif com.party_2 == old_id:
                    com.party_2 = new_id
                sess.add(com)

        if actually_do_it:
            sess.commit()

    # FUNDING P2P DEPENDENCIES
    sql_query = select(FundingPersonPerson).where(
        or_(
            FundingPersonPerson.party_1 == old_id,
            FundingPersonPerson.party_2 == old_id,
        )
    )
    fundingp2p_to_update = sess.exec(sql_query).all()
    if len(fundingp2p_to_update) > 0:
        print(
            "\t\t\t\tthe following funding p2p should be updated:"
        )
        for fp2p in fundingp2p_to_update:
            print(f"\t\t\t\t\t{fp2p}")
            if actually_do_it:
                if fp2p.party_1 == old_id:
                    fp2p.party_1 = new_id
                elif fp2p.party_2 == old_id:
                    fp2p.party_2 = new_id
                sess.add(fp2p)
        if actually_do_it:
            sess.commit()

    # FUNDING P2O DEPENDENCIES
    sql_query = select(FundingPersonOrg).where(
        FundingPersonOrg.person == old_id
    )
    fundingp2o_to_update = sess.exec(sql_query).all()
    if len(fundingp2o_to_update) > 0:
        print(
            "\t\t\t\tthe following funding p2o should be updated:"
        )
        for fp2o in fundingp2o_to_update:
            print(f"\t\t\t\t\t{fp2o}")
            if actually_do_it:
                fp2o.person = new_id
                sess.add(fp2o)
        if actually_do_it:
            sess.commit()

    # COMMUNICATIONSPERSONORG DEPENDENCIES
    sql_query = select(CommunicationsPersonOrg).where(
        CommunicationsPersonOrg.person == old_id
    )
    commsp2o_to_update = sess.exec(sql_query).all()
    if len(commsp2o_to_update) > 0:
        print(
            "\t\t\t\tthe following comms p2o should be updated:"
        )
        for commsp2o in commsp2o_to_update:
            print(f"\t\t\t\t\t{commsp2o}")
            if actually_do_it:
                commsp2o.person = new_id
                sess.add(commsp2o)
        if actually_do_it:
            sess.commit()

    # VOTEINDIVIDUAL DEPENDENCIES
    sql_query = select(VoteIndividual).where(
        VoteIndividual.person == old_id
    )
    vote_to_update = sess.exec(sql_query).all()
    if len(vote_to_update) > 0:
        print(
            "\t\t\t\tthe following voteindividual should be updated:"
        )
        for vote in vote_to_update:
            print(f"\t\t\t\t\t{vote}")
            if actually_do_it:
                vote.person = new_id
                sess.add(vote)
        if actually_do_it:
            sess.commit()

    if actually_do_it:
        finally_delete = sess.exec(
            select(Person).where(Person.id == old_id)
        ).first()
        sess.delete(finally_delete)
        sess.commit()
