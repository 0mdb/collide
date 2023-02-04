"""
This script is looking for shortened versions of first names, e.g. James vs Jim and merge the entries using the
'more proper' version
"""
from schema_creation.sqlmodel_build import (
    Person,
)
from sqlmodel import select
from common_func import create_match_name, create_session
from fix_people_000_common import first_name_synonyms, most_proper
import fix_funcs


def fix_people_003(debug_status):
    """Amends Person table entries, substituting common first name synonyms (e.g. Will, William).

    Parameters
    ----------
    debug_status

    Returns
    -------
    Nothing

    """
    actually_do_it = True
    sess = create_session(debug_status)

    kl = list(first_name_synonyms.keys())
    for n in kl:
        l = first_name_synonyms[n]
        for sl in l:
            new_l = l.copy()
            nk = sl
            new_l.remove(nk)
            new_l.append(n)
            first_name_synonyms[nk] = new_l

    sql_query = select(Person)
    res = sess.exec(sql_query).all()

    for p in res:

        nt = p.display_name.split(" ")
        nt = [x[:-1] if x.endswith(",") else x for x in nt]

        if nt[0] in first_name_synonyms.keys():
            print(
                f"Name synonyms exist for {p.display_name}"
            )

            potential_names = []
            for name in first_name_synonyms[nt[0]]:
                potential_names.append(" ".join([name] + nt[1:]))

                for q in potential_names:
                    # print(f"\tpotential name: {q}")
                    sql_query = select(Person).where(
                        Person.match_name == create_match_name(q)
                    )
                    res = sess.exec(sql_query).all()
                    if len(res) > 0:
                        lon = [nt[0]] + first_name_synonyms[nt[0]]
                        most_proper_first_name = [x for x in lon if x in most_proper]

                        name_to_go_with = " ".join(most_proper_first_name + nt[1:])

                        sql_query = select(Person).where(
                            Person.match_name == create_match_name(name_to_go_with)
                        )
                        keep_person = sess.exec(sql_query).first()

                        if keep_person is None:
                            print(
                                f"no entries in preferred name {create_match_name(name_to_go_with)}, skipping"
                            )
                        else:
                            print(
                                f"we are going to keep {keep_person.display_name} (id {keep_person.id})"
                            )

                            for alt_first_name in first_name_synonyms[
                                most_proper_first_name[0]
                            ]:
                                other_name = " ".join([alt_first_name] + nt[1:])
                                sql_query = select(Person).where(
                                    Person.match_name == create_match_name(other_name)
                                )
                                res = sess.exec(sql_query).first()
                                if res is not None:
                                    print(
                                        f"\twe are going to get rid of {res.display_name} (id {res.id})"
                                    )
                                    fix_funcs.replace_person(
                                        old_id=res.id,
                                        new_id=keep_person.id,
                                        sess=sess,
                                        actually_do_it=actually_do_it
                                    )

    sess.close()

    #
    # print(f"{p.display_name}")
    # print(f"\t\tdatabase hit for {res[0].display_name}")

    # sql_query = select(Person).where(col(Person.match_name).contains(p.match_name))
    # loc_res = sess.exec(sql_query).all()
    #
    # if len(loc_res) > 1:  # we have more than one name to deal with
    #     # redo the current match_name
    #
    #     redone_match_name = create_match_name(' '.join(nt))
    #
    #     name_lengths = {}
    #
    #     print(f"{p.display_name} (id: {p.id})")
    #     f = []
    #     for pp in loc_res:
    #
    #         print(f"\t{pp.display_name} (id: {pp.id})")
    #
    #         name_tokens = pp.display_name.split(" ")  # split on spaces
    #         name_tokens = [x[:-1] if x.endswith(',') else x for x in name_tokens]  # strip trailing commas
    #
    #         name_tokens = [x for x in name_tokens if x.lower() not in shit_list_combined]
    #         new_match_name = create_match_name(" ".join(name_tokens))
    #         if new_match_name == redone_match_name:
    #             print("\tmarked equivalent")
    #             name_lengths[pp.id] = (len(pp.display_name), pp.display_name)
    #             if pp.id != p.id:
    #                 f.append(pp)
    #
    #     if len(name_lengths.keys()) > 1:
    #         print('\t\tsome redundancies to remove')
    #         srted = dict(sorted(name_lengths.items(), key=lambda item: item[1][0]))
    #
    #         id_to_keep = list(srted.keys())[0]
    #         name_to_keep = srted[id_to_keep][1]
    #         print(f"\t\tkeeping {name_to_keep} (id: {id_to_keep})")
    #
    #         id_list_to_remove = list(srted.keys())[1:]
    #         for rem in id_list_to_remove:
    #             print(f"\t\t\tremoval of {srted[rem][1]} (id: {rem})")
    #
    #             sql_query = select(OrganizationMembership).where(OrganizationMembership.person == rem)
    #             memberships_to_update = sess.exec(sql_query).all()
    #             if len(memberships_to_update) > 0:
    #                 print("\t\t\t\tthe following memberships should be updated:")
    #                 for mem in memberships_to_update:
    #                     print(f"\t\t\t\t\t{mem}")
    #                     mem.person = id_to_keep
    #                     sess.add(mem)
    #                 sess.commit()
    #
    #             sql_query = select(Communications).where(or_(Communications.party_1 == rem, Communications.party_2 == rem))
    #             communications_to_update = sess.exec(sql_query).all()
    #             if len(communications_to_update) > 0:
    #                 print("\t\t\t\tthe following communications should be updated:")
    #                 for com in communications_to_update:
    #                     print(f"\t\t\t\t\t{com}")
    #                     if com.party_1 == rem:
    #                         com.party_1 = id_to_keep
    #                     elif com.party_2 == rem:
    #                         com.party_2 = id_to_keep
    #                     sess.add(com)
    #
    #                 sess.commit()
    #
    #             finally_delete = sess.exec(select(Person).where(Person.id == rem)).first()
    #             sess.delete(finally_delete)
    #             sess.commit()
