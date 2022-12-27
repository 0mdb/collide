from fuzzywuzzy import fuzz
from operator import itemgetter
from schema_creation.sqlmodel_build import Person, OrganizationMembership, Communications
from sqlmodel import create_engine, select, Session, col, or_
from sqlalchemy import func

from parse_injest.utils import create_match_name

db_host = "192.168.0.10"
db_name = "collide"
db_user = "test_user"
db_pw = "change_this"

schema_name = "lf_mockup_2"

engine = create_engine(f"postgresql+psycopg2://{db_user}:{db_pw}@{db_host}/{db_name}", echo=False)
sess = Session(engine)

all_people = sess.exec(select(Person)).all()

while len(all_people) > 0:
    current_person = all_people.pop()

    high_fuzz = []
    for p in all_people:
        rat = fuzz.ratio(current_person.match_name, p.match_name)
        if rat > 95:
            high_fuzz.append((rat, p))

    if len(high_fuzz) > 0:
        high_fuzz = sorted(high_fuzz, key=itemgetter(0))

        cp_mem = sess.query(OrganizationMembership).where(OrganizationMembership.person == current_person.id).count()
        cp_com = sess.query(Communications).where(or_(Communications.party_1 == current_person.id, Communications.party_2 == current_person.id)).count()

        print(f"{current_person.display_name}, id {current_person.id}, {cp_mem} memberships, {cp_com} communications matches highly with:")

        for hf in high_fuzz:

            hf_mem = sess.query(OrganizationMembership).where(OrganizationMembership.person == hf[1].id).count()
            hf_com = sess.query(Communications).where(or_(Communications.party_1 == hf[1].id, Communications.party_2 == hf[1].id)).count()

            print(f"\t{hf[1].display_name}, id {hf[1].id}, {hf_mem} memberships, {hf_com} communications ({hf[0]})")


sess.close()