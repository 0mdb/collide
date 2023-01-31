"""
This script looks for the problem of a match name and a display name not following from one another.  This
sometimes creeps in from other fixes
"""
from schema_creation.sqlmodel_build import Person
from sqlmodel import select
from common_func import create_match_name, create_session


def fix_people_006(debug_status):
    actually_do_it = True
    sess = create_session(debug_status)

    sql_query = select(Person)

    res = sess.exec(sql_query).all()

    total_problems = 0
    for p in res:

        dn = p.display_name
        mn = p.match_name
        if mn != create_match_name(dn):
            print(p)
            if actually_do_it:
                p.match_name = create_match_name(dn)
                sess.add(p)
                sess.commit()
            total_problems += 1

    sess.close()

    print(f"total problems was {total_problems}")
