from schema_creation.sqlmodel_build import (
    Person,
    OrganizationMembership,
    Communications,
    Organization,
)
from sqlmodel import create_engine, select, Session, or_
import pickle

from parse_injest.utils import create_match_name

db_host = "localhost"
db_name = "lq_test"
db_user = "test_user"
db_pw = "change_this"

engine = create_engine(
    f"postgresql+psycopg2://{db_user}:{db_pw}@{db_host}/{db_name}", echo=False
)
sess = Session(engine)

person_of_interest = "ALEXANDER POURBAIX"
person_of_interest_mn = create_match_name(person_of_interest)

num_people = 0
num_orgs = 0
num_links = 0

pile = []

nodes = {}
links = []

sql_query = select(Person.id).where(Person.match_name == person_of_interest_mn)
res = sess.exec(sql_query).first()

q = {
    "id": person_of_interest_mn,
    "name": person_of_interest,
    "person": True,
    "db_id": res,
}
nodes[person_of_interest_mn] = q
pile.append(q)

num_people += 1

while len(pile) > 0:
    # print(f"size of the pile is {len(pile)}")
    n = pile.pop()

    is_person = n["person"]
    db_id = n["db_id"]

    if is_person:
        # get any memberships
        sql_query = select(OrganizationMembership).where(
            OrganizationMembership.person == db_id
        )
        memberships = sess.exec(sql_query)

        for m in memberships:
            sql_query = select(Organization).where(Organization.id == m.organization)
            org = sess.exec(sql_query).first()
            temp = {
                "id": org.match_name,
                "name": org.display_name,
                "person": False,
                "db_id": org.id,
            }
            if org.match_name not in nodes.keys():
                nodes[org.match_name] = temp
                pile.append(temp)
                num_orgs += 1

            tl = {"source": org.match_name, "target": n["id"]}
            lt = {"source": n["id"], "target": org.match_name}
            if not (tl in links and lt in links):
                links.append(tl)
                num_links += 1

        # get any communications
        sql_query = select(Communications).where(
            or_(Communications.party_1 == db_id, Communications.party_2 == db_id)
        )
        communications = sess.exec(sql_query)
        for c in communications:
            if c.party_1 == db_id:
                other_side = c.party_2
            else:
                other_side = c.party_1

            sql_query = select(Person).where(Person.id == other_side)
            other_party = sess.exec(sql_query).first()

            if other_party.match_name not in nodes.keys():
                temp = {
                    "id": other_party.match_name,
                    "name": other_party.display_name,
                    "person": True,
                    "db_id": other_party.id,
                }
                nodes[other_party.match_name] = temp
                pile.append(temp)
                num_people += 1

            lt = {"source": other_party.match_name, "target": n["id"]}
            tl = {"source": n["id"], "target": other_party.match_name}
            if not (lt in links and tl in links):
                links.append(lt)
                num_links += 1

    else:  # if not a person, then this is an org
        sql_query = select(Organization).where(Organization.id == db_id)
        org = sess.exec(sql_query).first()

        if (
            org.match_name not in nodes.keys()
        ):  # we should never hit this since everything on the pile should already exist
            temp = {
                "id": org.match_name,
                "name": org.display_name,
                "person": False,
                "db_id": org.id,
            }
            nodes[org.match_name] = temp
            pile.append(temp)
            num_orgs += 1

        # get any parent organizations
        if org.parent_organization is not None:
            sql_query = select(Organization).where(
                Organization.id == org.parent_organization
            )
            parent = sess.exec(sql_query).first()

            if parent.match_name not in nodes.keys():
                temp = {
                    "id": parent.match_name,
                    "name": parent.display_name,
                    "person": False,
                    "db_id": parent.id,
                }
                nodes[parent.match_name] = temp
                pile.append(temp)
                num_orgs += 1

            tl = {"source": parent.match_name, "target": n["id"]}
            lt = {"source": n["id"], "target": n["id"]}
            if not (tl in links or lt in links):
                links.append(tl)
                num_links += 1

        # get any organization members
        sql_query = select(OrganizationMembership).where(
            OrganizationMembership.organization == db_id
        )
        memberships = sess.exec(sql_query)
        for m in memberships:
            sql_query = select(Person).where(Person.id == m.person)
            person = sess.exec(sql_query).first()

            if person.match_name not in nodes.keys():
                temp = {
                    "id": person.match_name,
                    "name": person.display_name,
                    "person": True,
                    "db_id": person.id,
                }
                nodes[person.match_name] = temp
                pile.append(temp)
                num_people += 1

            tl = {"source": person.match_name, "target": n["id"]}
            lt = {"source": n["id"], "target": person.match_name}
            if not (tl in links or lt in links):
                links.append(tl)
                num_links += 1

sess.close()

nodes = [x[1] for x in nodes.items()]

graph = {"nodes": nodes, "links": links}

with open("sample_graph.pickle", "wb") as pik:
    pickle.dump(graph, pik, pickle.HIGHEST_PROTOCOL)

print("all done")
print(f"we started with {person_of_interest} and...")
print(
    f"we managed to hit {num_orgs} organizations and {num_people} people with {num_links} total links"
)
