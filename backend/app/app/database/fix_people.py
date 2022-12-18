from schema_creation.sqlmodel_build import Person, OrganizationMembership, Communications
from sqlmodel import create_engine, select, Session, col, or_

from parse_injest.utils import create_match_name

shit_list_pref = ["Mr.",
                  "Ms.",
                  "Mrs.",
                  "Dr.",
                  "Hon.",
                  "Hon",
                  "Min.",
                  "The",
                  "Rt.",
                  "Right",
                  "Honourable",
                  "Honorable",
                  "Admiral",
                  "VAdm.",
                  "Senator",
                  'Minister',
                  'Monsieur',
                  "L'honorable",
                  "L’honorable",
                  "Honoruable",
                  "Honorable/Honorable",
                  "Hon.)",
                  "(The",
                  "L'hon.",
                  "l'hon",
                  "Ho.",
                  "CFNE",
                  "P.C.,M.P.",
                  "L'Hhonorable",
                  "H.E.",
                  "His",
                  "Excellency",
                  "Commodore",
                  "LGen",
                  "Major",
                  "General",
                  "Brigadier-General",
                  "Brigadier",
                  "Vice",
                  "Admiral",
                  "Rear-Admiral",
                  '']

shit_list_suff = ["P.C.",
                  "M.P.",
                  "P.C",
                  "M.P",
                  "MP",
                  "PC",
                  "Ph.D",
                  "PhD"]


shit_list_pref_lower = [x.lower() for x in shit_list_pref]
shit_list_suff_lower = [x.lower() for x in shit_list_suff]

shit_list_combined = shit_list_pref_lower.copy()
shit_list_combined.extend(shit_list_suff_lower)

db_host = "localhost"
db_name = "lq_test"
db_user = "test_user"
db_pw = "change_this"

schema_name = "lf_mockup_2"

engine = create_engine(f"postgresql+psycopg2://{db_user}:{db_pw}@{db_host}/{db_name}", echo=False)
sess = Session(engine)

sql_query = select(Person)

res = sess.exec(sql_query).all()


for p in res:

    sql_query = select(Person).where(col(Person.match_name).contains(p.match_name))
    loc_res = sess.exec(sql_query).all()

    if len(loc_res) > 1:  # we have more than one name to deal with
        # redo the current match_name
        nt = p.display_name.split(" ")
        nt = [x[:-1] if x.endswith(',') else x for x in nt]
        nt = [x for x in nt if x.lower() not in shit_list_combined]
        redone_match_name = create_match_name(' '.join(nt))

        name_lengths = {}

        print(f"{p.display_name} (id: {p.id})")
        f = []
        for pp in loc_res:

            print(f"\t{pp.display_name} (id: {pp.id})")

            name_tokens = pp.display_name.split(" ")  # split on spaces
            name_tokens = [x[:-1] if x.endswith(',') else x for x in name_tokens]  # strip trailing commas

            name_tokens = [x for x in name_tokens if x.lower() not in shit_list_combined]
            new_match_name = create_match_name(" ".join(name_tokens))
            if new_match_name == redone_match_name:
                print("\tmarked equivalent")
                name_lengths[pp.id] = (len(pp.display_name), pp.display_name)
                if pp.id != p.id:
                    f.append(pp)

        if len(name_lengths.keys()) > 1:
            print('\t\tsome redundancies to remove')
            srted = dict(sorted(name_lengths.items(), key=lambda item: item[1][0]))

            id_to_keep = list(srted.keys())[0]
            name_to_keep = srted[id_to_keep][1]
            print(f"\t\tkeeping {name_to_keep} (id: {id_to_keep})")

            id_list_to_remove = list(srted.keys())[1:]
            for rem in id_list_to_remove:
                print(f"\t\t\tremoval of {srted[rem][1]} (id: {rem})")

                sql_query = select(OrganizationMembership).where(OrganizationMembership.person == rem)
                memberships_to_update = sess.exec(sql_query).all()
                if len(memberships_to_update) > 0:
                    print("\t\t\t\tthe following memberships should be updated:")
                    for mem in memberships_to_update:
                        print(f"\t\t\t\t\t{mem}")
                        mem.person = id_to_keep
                        sess.add(mem)
                    sess.commit()

                sql_query = select(Communications).where(or_(Communications.party_1 == rem, Communications.party_2 == rem))
                communications_to_update = sess.exec(sql_query).all()
                if len(communications_to_update) > 0:
                    print("\t\t\t\tthe following communications should be updated:")
                    for com in communications_to_update:
                        print(f"\t\t\t\t\t{com}")
                        if com.party_1 == rem:
                            com.party_1 = id_to_keep
                        elif com.party_2 == rem:
                            com.party_2 = id_to_keep
                        sess.add(com)

                    sess.commit()

                finally_delete = sess.exec(select(Person).where(Person.id == rem)).first()
                sess.delete(finally_delete)
                sess.commit()
