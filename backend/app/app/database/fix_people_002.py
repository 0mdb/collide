import titlecase
from schema_creation.sqlmodel_build import Person, OrganizationMembership, Communications
from sqlmodel import create_engine, select, Session, col, or_

from parse_injest.utils import create_match_name

from fix_people_000_common import shit_list_combined

db_host = "192.168.0.10"
db_name = "collide"
db_user = "test_user"
db_pw = "change_this"

schema_name = "lf_mockup_2"

engine = create_engine(f"postgresql+psycopg2://{db_user}:{db_pw}@{db_host}/{db_name}", echo=False)
sess = Session(engine)

sql_query = select(Person)

res = sess.exec(sql_query).all()
total_changes = 0
total_problems = 0

for p in res:
    orig_display_name = p.display_name
    nt = p.display_name.split(" ")
    nt = [x[:-1] if x.endswith(',') else x for x in nt]
    nt = [x.strip() for x in nt]
    nt = [x for x in nt if x.lower() not in shit_list_combined]

    nt = " ".join(nt)
    nt = titlecase.titlecase(nt)

    if nt != orig_display_name:
        print(f"changing {orig_display_name} to {nt}")
        new_match_name = create_match_name(nt)
        sql_query = select(Person).where(Person.match_name == new_match_name).where(Person.id != p.id)
        res_1 = sess.exec(sql_query).all()
        sql_query = select(Person).where(Person.display_name == nt)
        res_2 = sess.exec(sql_query).all()

        if len(res_1) > 0 or len(res_2) > 0:
            print("this change will cause problems")
            print(f"{p}")
            print(f"{res_1}")
            print(f"{res_2}")
            total_problems += 1
        else:

            total_changes += 1
            p.display_name = nt
            p.match_name = create_match_name(nt)
            sess.add(p)
            sess.commit()

sess.close()
print(f"total changes {total_changes}, total problems {total_problems}")