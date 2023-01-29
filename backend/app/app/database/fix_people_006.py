"""
This script looks for the problem of a match name and a display name not following from one another.  This
sometimes creeps in from other fixes
"""
from schema_creation.sqlmodel_build import Person
from sqlmodel import create_engine, select, Session

from common_func import create_match_name

db_host = "192.168.0.10"
db_name = "collide"
db_user = "test_user"
db_pw = "change_this"

schema_name = "lf_mockup_2"

actually_do_it = False

engine = create_engine(
    f"postgresql+psycopg2://{db_user}:{db_pw}@{db_host}/{db_name}", echo=False
)
sess = Session(engine)

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
