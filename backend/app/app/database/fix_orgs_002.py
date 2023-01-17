"""
This script looks for different orgs that have limited/ltd and incorporated/inc names and merges them
"""
import json
from sqlmodel import select
from schema_creation.sqlmodel_build import Organization
from common_func import create_session
from fix_funcs import replace_organization


def get_org_summary(org: Organization):
    s = {
        "id": org.id,
        "match_name": org.match_name,
        "display_name": org.display_name,
        "sector": org.sector,
        "type": org.organization_type,
        "parent": org.parent_organization,
        "source": org.source,
    }
    return s


if __name__ == "__main__":
    sess = create_session(db_name="collide", db_host="192.168.0.10")

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
            if "limited" in mn:
                swapped_mn = mn.replace("limited", "ltd")
            elif "ltd" in mn:
                swapped_mn = mn.replace("ltd", "limited")

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
            if "inc" in mn:
                swapped_mn = mn.replace("inc", "incorporated")
            elif "incorporated" in mn:
                swapped_mn = mn.replace("incorporated", "inc")
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

    # figure out which version has more data, keep that one even if we need to change the name
    for k in chnglist.keys():
        first, second = chnglist[k]

        move_org_type = False
        best_org_type = first["organization_type"]
        if first["organization_type"] == 6 and second["organization_type"] != 6:
            best_org_type = second["organization_type"]
            move_org_type = True

        move_parent_org = False
        best_parent_org = first["parent_organization"]
        if (
                first["organization_type"] is None
                and second["parent_organization"] is not None
        ):
            best_parent_org = second["parent_organization"]
            move_parent_org = True

        move_sector = False
        best_sector = first["sector"]
        if first["sector"] is None and second["sector"] is not None:
            best_sector = second["sector"]
            move_sector = True

        move_misc_data = True
        best_misc_data = first["misc_data"] | second["misc_data"]

        if "ltd" in first["match_name"] or "inc" in first["match_name"]:
            id_to_keep = first["id"]
            id_to_remove = second["id"]
        else:
            id_to_keep = second["id"]
            id_to_remove = first["id"]

        sq = select(Organization).where(Organization.id == id_to_keep)
        res = sess.exec(sq).first()

        res.parent_organization = best_parent_org
        res.sector = best_sector
        res.organization_type = best_org_type
        res.misc_data = best_misc_data
        sess.add(res)
        sess.commit()

        replace_organization(id_to_remove, id_to_keep, sess, True)

    sess.close()

    with open("fix_orgs_002_changelist.json", "w") as h:
        json.dump(chnglist, h, indent=4)

    if actually_do_it:
        w = " were "
    else:
        w = " would have been "
    print(f"number of changes that{w}made was: {num_changes}")
