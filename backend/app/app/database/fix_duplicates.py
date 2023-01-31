from schema_creation.sqlmodel_build import (
    OrganizationMembership,
    Communications,
)
from sqlmodel import select
from common_func import create_session


def fix_duplicates(debug_status):
    sess = create_session(debug_status)
    do_removal = True

    print("##### MEMBERSHIPS #####")

    # check for memberships that are duplicates
    sql_query = select(OrganizationMembership)
    res = sess.exec(sql_query)
    for mem in res:

        sql_query = (
            select(OrganizationMembership)
            .where(OrganizationMembership.person == mem.person)
            .where(OrganizationMembership.organization == mem.organization)
            .where(OrganizationMembership.start_date == mem.start_date)
            .where(OrganizationMembership.end_date == mem.end_date)
            .where(OrganizationMembership.source == mem.source)
            .where(OrganizationMembership.id != mem.id)
        )
        matches = sess.exec(sql_query).all()
        if len(matches) >= 1:
            print(f"possible duplicate of {mem}")
            for m in matches:
                print(f"\t{m}")
                if do_removal:
                    print(f"\tremoving {m}")
                    sess.delete(m)
                    sess.commit()

    print("##### COMMUNICATIONS #####")
    # check for communications that are duplicates
    sql_query = select(Communications)
    res = sess.exec(sql_query)
    for com in res:
        sql_query = (
            select(Communications)
            .where(Communications.party_1 == com.party_1)
            .where(Communications.party_2 == com.party_2)
            .where(Communications.com_date == com.com_date)
            .where(Communications.topic == com.topic)
            .where(Communications.source == com.source)
            .where(Communications.id != com.id)
        )
        matches = sess.exec(sql_query).all()
        if len(matches) >= 1:
            print(f"possible duplicate of {com}")
            for m in matches:
                print(f"\t{m}")
                if do_removal:
                    print(f"\tremoving {m}")
                    sess.delete(m)
                    sess.commit()
    sess.close()
