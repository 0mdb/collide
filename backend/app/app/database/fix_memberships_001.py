from schema_creation.sqlmodel_build import (
    OrganizationMembership,
)
from sqlmodel import select
from common_func import create_session


def fix_memberships_001(debug_status):
    sess = create_session(debug_status)

    memberships = sess.exec(select(OrganizationMembership)).all()

    while len(memberships) > 0:

        m = memberships.pop()

        # search for all memberships between this person and organization that aren't this one we are starting with
        sql_query = (
            select(OrganizationMembership)
            .where(OrganizationMembership.person == m.person)
            .where(OrganizationMembership.organization == m.organization)
            .where(OrganizationMembership.id != m.id)
            # .where(OrganizationMembership.source != 7)
        )
        memberships_to_merge = sess.exec(sql_query).all()
        if len(memberships_to_merge) > 0:
            earliest_start_date = m.start_date
            latest_end_date = m.end_date
            print(f"equivalent memberships {m}")
            ids_to_remove = []
            for q in memberships_to_merge:
                print(f"\t{q}")
                ids_to_remove.append(q.id)
                if q.start_date < earliest_start_date:
                    earliest_start_date = q.start_date
                if q.end_date > latest_end_date:
                    latest_end_date = q.end_date

                try:
                    memberships.remove(q)
                except Exception as e:
                    print(f"\t\ttried to remove {q} from master list, got an exception {e}")

                if m.start_date != earliest_start_date or m.end_date != latest_end_date:
                    print(f"\t\texpanding out the dates")

                m.start_date = earliest_start_date
                m.end_date = latest_end_date

                sess.add(m)

                for i in ids_to_remove:
                    finally_delete = sess.exec(
                        select(OrganizationMembership).where(OrganizationMembership.id == i)
                    ).first()
                    if finally_delete is not None:
                        sess.delete(finally_delete)

                sess.commit()

    sess.close()
