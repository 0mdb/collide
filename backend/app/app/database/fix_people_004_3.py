from schema_creation.sqlmodel_build import Person, Organization
from sqlmodel import create_engine, select, Session
import pickle
import sqlalchemy as sa
import json

if __name__ == "__main__":

    db_host = "192.168.0.10"
    db_name = "collide"
    db_user = "test_user"
    db_pw = "change_this"

    schema_name = "lf_mockup_2"

    flag = 'org'

    pickle_name = f"spelling_check_{flag}.pickle"
    json_name = f"spelling_check_{flag}.json"

    if flag == 'org':
        t = Organization
    elif flag == "person":
        t = Person
    else:
        raise NotImplementedError(f"can't do {flag} yet")

    engine = create_engine(f"postgresql+psycopg2://{db_user}:{db_pw}@{db_host}/{db_name}", echo=False)
    sess = Session(engine)

    all_people = sess.exec(select(t)).all()

    d_people = {}
    for p in all_people:
        d_people[p.match_name] = {'id': p.id, "display_name": p.display_name, "match_name": p.match_name}

    fuzzy_matches = {}
    stop = False  # stop when we run out of people to check
    while not stop:
        cmn, d = d_people.popitem()
        sq = select(t).where(sa.func.levenshtein_less_equal(cmn, t.match_name, 2) <= 2)
        res = sess.exec(sq).all()

        if len(res) > 1:
            fuzzy_matches[cmn] = []
            fuzzy_matches[cmn].append(d)
            for m in res:
                if m.match_name != cmn:
                    try:
                        q = d_people.pop(m.match_name)
                        fuzzy_matches[cmn].append(q)
                    except KeyError:
                        print(f"{m.match_name} already matched to another entry")

        if len(d_people) == 0:
            stop = True

    with open(pickle_name, 'wb') as h:
        pickle.dump(fuzzy_matches, h, pickle.HIGHEST_PROTOCOL)
    with open(json_name, 'w') as h:
        json.dump(fuzzy_matches, h, indent=4)
