from schema_creation.sqlmodel_build import (
    OrganizationMembership,
    Communications,
)
from sqlmodel import create_engine, select, Session

do_removal = True

db_host = "192.168.0.10"
db_name = "collide"
db_user = "test_user"
db_pw = "change_this"

schema_name = "lf_mockup_2"

engine = create_engine(
    f"postgresql+psycopg2://{db_user}:{db_pw}@{db_host}/{db_name}", echo=False
)
sess = Session(engine)

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
