from schema_creation.sqlmodel_build import Person, OrganizationMembership, Communications
from sqlmodel import create_engine, select, Session, col, or_

from parse_injest.utils import create_match_name

db_host = "192.168.0.10"
db_name = "collide"
db_user = "test_user"
db_pw = "change_this"

schema_name = "lf_mockup_2"

engine = create_engine(f"postgresql+psycopg2://{db_user}:{db_pw}@{db_host}/{db_name}", echo=False)
sess = Session(engine)

all_people = sess.exec(select(Person)).all()

for person in all_people:

    dn = person.display_name

    dn_tokens = dn.split(" ")

    # reverse the order of the name
    dn_tokens.reverse()
    reversed_dn = " ".join(dn_tokens)
    reversed_mn = create_match_name(reversed_dn)

    # check for an entry of the reversed name
    sql_query = select(Person).where(Person.match_name == reversed_mn)
    res = sess.exec(sql_query).first()

    if res is not None:
        forward_mem = sess.query(OrganizationMembership).where(OrganizationMembership.person == person.id).count()
        forward_com = sess.query(Communications).where(or_(Communications.party_1 == person.id, Communications.party_2 == person.id)).count()
        backward_mem = sess.query(OrganizationMembership).where(OrganizationMembership.person == res.id).count()
        backward_com = sess.query(Communications).where(or_(Communications.party_1 == res.id, Communications.party_2 == res.id)).count()
        print(f"{dn} is also in the database as {reversed_dn}")
        print(f"\tforward mem {forward_mem}, forward com {forward_com}")
        print(f"\tbackward mem {backward_mem}, backward com {backward_com}")


sess.close()