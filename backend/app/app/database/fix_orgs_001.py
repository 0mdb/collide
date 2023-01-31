from sqlmodel import select
from schema_creation.sqlmodel_build import (
    Organization
)
from common_func import create_session


def fix_orgs_001(debug_status):
    sess = create_session(debug_status)
    actually_do_it = True

    num_changes = 0

    sq = select(Organization)
    orgs = sess.exec(sq)
    for o in orgs:
        dn = o.display_name
        sdn = dn.strip()
        if dn != sdn:
            num_changes += 1
            if actually_do_it:
                o.display_name = sdn
                sess.add(o)
                sess.commit()

    sess.close()
    if actually_do_it:
        w = ' were '
    else:
        w = " would have been "
    print(f"number of changes that{w}made was: {num_changes}")
