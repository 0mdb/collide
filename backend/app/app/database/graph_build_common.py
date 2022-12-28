from schema_creation.sqlmodel_build import (
    Person,
    OrganizationMembership,
    Communications,
    Organization,
    SectorIndustry,
    Funding,
    FundingPersonOrg,
    FundingPersonPerson,
    CommunicationsPersonOrg,
    CommunicationsOrgOrg,
)
from sqlmodel import create_engine, select, Session, or_


def check_and_add_organization(db_sess, list_of_nodes, pile_list, depth_list, curr_depth, org_db_id):
    sql_query = select(Organization).where(Organization.id == org_db_id)
    org = db_sess.exec(sql_query).first()
    if org.sector is not None:
        sql_query = select(SectorIndustry).where(SectorIndustry.id == org.sector)
        res = db_sess.exec(sql_query).first()
        sec = res.sector_display_name
        ind = res.industry_display_name
        tot = f"{sec},{ind}"
    else:
        tot = None

    if org.match_name not in list_of_nodes.keys():
        temp = {
            "id": org.match_name,
            "name": org.display_name,
            "val": 6,
            'sector': tot,
            "person": False,
            "db_id": org.id,
        }
        list_of_nodes[org.match_name] = temp
        pile_list.append(temp)
        depth_list.append(curr_depth + 1)
        return_int = 1
    else:
        return_int = 0
    return return_int, org.match_name


def check_and_add_person(db_sess, list_of_nodes, pile_list, depth_list, curr_depth, person_db_id):
    sql_query = select(Person).where(Person.id == person_db_id)
    p = db_sess.exec(sql_query).first()

    if p.match_name not in list_of_nodes.keys():
        temp = {
            "id": p.match_name,
            "name": p.display_name,
            "person": True,
            "db_id": p.id,
        }
        list_of_nodes[p.match_name] = temp
        pile_list.append(temp)
        depth_list.append(curr_depth + 1)
        return_int = 1
    else:
        return_int = 0
    return return_int, p.match_name