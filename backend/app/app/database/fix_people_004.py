"""
This script is for finding likely spelling mistakes, but has been superseded by the version in fix_people_004_3
"""
from fuzzywuzzy import fuzz
from operator import itemgetter
from schema_creation.sqlmodel_build import (
    Person,
    OrganizationMembership,
    Communications,
)
from sqlmodel import create_engine, select, Session, col, or_
import pickle

import concurrent.futures

from common_func import create_match_name


def fuzz_helper(it):
    mn = it[0]
    pl = it[1]

    high_fuzz = []
    for p in pl:
        rat = fuzz.ratio(mn, p.match_name)
        if rat > 95:
            high_fuzz.append((rat, p))
    if len(high_fuzz) > 0:
        high_fuzz = sorted(high_fuzz, key=itemgetter(0))
    return mn, high_fuzz


if __name__ == "__main__":

    db_host = "192.168.0.10"
    db_name = "collide"
    db_user = "test_user"
    db_pw = "change_this"

    schema_name = "lf_mockup_2"

    pickle_name = "spelling_check.pickle"

    engine = create_engine(
        f"postgresql+psycopg2://{db_user}:{db_pw}@{db_host}/{db_name}", echo=False
    )
    sess = Session(engine)

    all_people = sess.exec(select(Person)).all()

    fuzzy_ratios = {}
    threaded_inputs = [(n.match_name, all_people) for n in all_people]

    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor:
        for n, hf in executor.map(fuzz_helper, threaded_inputs):
            fuzzy_ratios[n] = hf

    for mn in fuzzy_ratios.keys():
        fuzz_list = fuzzy_ratios[mn]
        if len(fuzz_list) > 1:

            cp = sess.exec(select(Person).where(Person.match_name == mn)).first()
            cp_mem = (
                sess.query(OrganizationMembership)
                .where(OrganizationMembership.person == cp.id)
                .count()
            )
            cp_com = (
                sess.query(Communications)
                .where(
                    or_(
                        Communications.party_1 == cp.id, Communications.party_2 == cp.id
                    )
                )
                .count()
            )

            print(
                f"{cp.display_name}, id {cp.id}, {cp_mem} memberships, {cp_com} communications matches highly with:"
            )

            for hf in fuzz_list:
                hf_mem = (
                    sess.query(OrganizationMembership)
                    .where(OrganizationMembership.person == hf[1].id)
                    .count()
                )
                hf_com = (
                    sess.query(Communications)
                    .where(
                        or_(
                            Communications.party_1 == hf[1].id,
                            Communications.party_2 == hf[1].id,
                        )
                    )
                    .count()
                )
                print(
                    f"\t{hf[1].display_name}, id {hf[1].id}, {hf_mem} memberships, {hf_com} communications ({hf[0]})"
                )

    sess.close()

    with open(pickle_name, "wb") as h:
        pickle.dump(fuzzy_ratios, h, pickle.HIGHEST_PROTOCOL)
