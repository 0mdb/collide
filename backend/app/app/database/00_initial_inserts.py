from sqlmodel import select
from parse_injest.utils import create_match_name
from schema_creation.sqlmodel_build import (
    OrganizationType,
    Organization,
    SectorIndustry,
)
from datetime import date
import common_func as cf


def insert_entries_for_fresh_db():
    """
    Run after tables have been created but no entries exist.
    Includes Organization, SectorIndustry, OrganizationType entries.

    Returns
    -------

    """

    org_type_list = [
        "Corporation",
        "Government",
        "Charity",
        "Professional Association",
        "Political Party",
        "Unclassified",
        "Trade Union"
    ]
    sector_list = ["Government"]
    org_list = {
        "Federal Government of Canada": {"type": "Government", "sector": "Government"}
    }

    session = cf.create_session(debug=True)

    for tn in org_type_list:

        stat = select(OrganizationType.id).where(
            OrganizationType.match_name == create_match_name(tn)
        )
        res = session.exec(stat).first()

        if res is None:
            ot = OrganizationType(display_name=tn, match_name=create_match_name(tn))
            session.add(ot)

    session.commit()

    for s in sector_list:
        stat = select(SectorIndustry.id).where(
            SectorIndustry.sector_match_name == create_match_name(s)
        )
        res = session.exec(stat).first()

        if res is None:
            sec = SectorIndustry(
                sector_display_name=s, sector_match_name=create_match_name(s)
            )
            session.add(sec)
    session.commit()

    for on in org_list.keys():
        stat = select(Organization.id).where(
            Organization.match_name == create_match_name(on)
        )
        res = session.exec(stat).first()

        if res is None:
            src_obj = cf.add_sources(session, [{"data_source": "initial inserts",
                                               "date_obtained": date.today()}])
            src_id = src_obj.id

            org_sec = org_list[on]["sector"]
            stat = select(SectorIndustry.id).where(
                SectorIndustry.sector_match_name == create_match_name(org_sec)
            )
            res = session.exec(stat).all()
            if len(res) == 0:
                raise RuntimeError("org sector not in database")
            org_sec_id = res[0]

            org_type = org_list[on]["type"]
            stat = select(OrganizationType.id).where(
                OrganizationType.match_name == create_match_name(org_type)
            )
            res = session.exec(stat).first()
            if res is None:
                raise RuntimeError("org type not in database")
            org_type_id = res

            orgo = Organization(
                display_name=on,
                match_name=create_match_name(on),
                organization_type=org_type_id,
                sector=org_sec_id,
                source=src_id,
            )
            session.add(orgo)
    session.commit()
    session.close()
