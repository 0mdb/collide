import json
from sqlmodel import select
from schema_creation.sqlmodel_build import (
    Organization
)
from common_func import create_session


def get_org_summary(org: Organization):
    s = {'id': org.id,
         'match_name': org.match_name,
         'display_name': org.display_name,
         'sector': org.sector,
         'type': org.organization_type,
         'parent': org.parent_organization,
         'source': org.source
         }
    return s


if __name__ == "__main__":
    sess = create_session(db_name='collide', db_host='192.168.0.10')

    chnglist = {}

    actually_do_it = False
    do_ltd_swap = True
    do_inc_swap = True
    num_changes = 0

    sq = select(Organization)
    orgs = sess.exec(sq)
    for o in orgs:
        mn = o.match_name

        if do_ltd_swap:
            swapped_mn = None
            if 'limited' in mn:
                swapped_mn = mn.replace('limited', 'ltd')
            elif 'ltd' in mn:
                swapped_mn = mn.replace('ltd', 'limited')

            if swapped_mn is not None:
                sq = select(Organization).where(Organization.match_name == swapped_mn)
                res = sess.exec(sq).first()  # there should only be one
                if res is not None:
                    if mn not in chnglist.keys() and swapped_mn not in chnglist.keys():
                        chnglist[mn] = []
                        if mn in chnglist.keys():
                            k = mn
                        else:
                            k = swapped_mn
                        chnglist[k].append(o.as_dict())
                        chnglist[k].append(res.as_dict())
                        num_changes += 1

        if do_inc_swap:
            swapped_mn = None
            if 'inc' in mn:
                swapped_mn = mn.replace('inc', 'incorporated')
            elif 'incorporated' in mn:
                swapped_mn = mn.replace('incorporated', 'inc')
            if swapped_mn is not None:
                sq = select(Organization).where(Organization.match_name == swapped_mn)
                res = sess.exec(sq).first()  # there should only be one
                if res is not None:
                    if mn not in chnglist.keys() and swapped_mn not in chnglist.keys():
                        chnglist[mn] = []
                        if mn in chnglist.keys():
                            k = mn
                        else:
                            k = swapped_mn
                        chnglist[k].append(o.as_dict())
                        chnglist[k].append(res.as_dict())
                        num_changes += 1

    sess.close()

    with open('fix_orgs_002_changelist.json', 'w') as h:
        json.dump(chnglist, h, indent=4)

    if actually_do_it:
        w = ' were '
    else:
        w = " would have been "
    print(f"number of changes that{w}made was: {num_changes}")
