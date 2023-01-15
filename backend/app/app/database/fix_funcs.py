from schema_creation.sqlmodel_build import OrganizationMembership, Organization, \
    CommunicationsOrgOrg, CommunicationsPersonOrg, OrganizationType, FundingPersonOrg, Funding
from sqlmodel import select
import common_func as cf


def return_preferred_party_name(match_name_in_question):
    bloc_name_set = {"blocquebecois", "blocquebecoiscaucus"}
    ndp_name_set = {"newdemocraticparty", "ndpcaucus", "ndp"}
    liberal_name_set = {"liberalpartyofcanada", "liberalcaucus", "liberal", "partiliberal",
                        "liberalpartyofcanadaofficialopposition"}
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

    # update communicationsorgorg party_1 links
    sql_query = select(CommunicationsOrgOrg).where(CommunicationsOrgOrg.party_1 == old_id)
    res = sess.exec(sql_query).all()

    for each_commsorgorg_p1 in res:
        each_commsorgorg_p1.party_1 = new_id

        if actually_do_it:
            sess.add(each_commsorgorg_p1)
            sess.commit()

    # update communicationsorgorg party_2 links
    sql_query = select(CommunicationsOrgOrg).where(CommunicationsOrgOrg.party_2 == old_id)
    res = sess.exec(sql_query).all()

    for each_commsorgorg_p2 in res:
        each_commsorgorg_p2.party_2 = new_id

        if actually_do_it:
            sess.add(each_commsorgorg_p2)
            sess.commit()

    # update communicationspersonorg links
    sql_query = select(CommunicationsPersonOrg).where(CommunicationsPersonOrg.organization == old_id)
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
    sql_query = select(OrganizationMembership).where(OrganizationMembership.organization == old_id)
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
        final_moments = sess.exec(select(Organization).where(Organization.id == old_id)).first()
        sess.delete(final_moments)
        sess.commit()
