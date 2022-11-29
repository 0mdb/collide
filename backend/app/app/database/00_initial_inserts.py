from sqlmodel import Session, create_engine, select, engine
from parse_injest.utils import create_match_name
from schema_creation.sqlmodel_build import (
    OrganizationType,
    Organization,
    SectorIndustry,
    Source,
)
from datetime import date


def ensure_source(eng: engine, sl: Source):
    sess = Session(eng)
    stat = (
        select(Source.id)
        .where(Source.data_source == sl.data_source)
        .where(Source.date_obtained == sl.date_obtained)
    )
    res = sess.exec(stat).all()

    if len(res) == 0:
        sess.add(sl)
        sess.commit()
        stat = (
            select(Source.id)
            .where(Source.data_source == sl.data_source)
            .where(Source.date_obtained == sl.date_obtained)
        )
        res = sess.exec(stat).all()
        sess.close()
        return res[0]
    else:
        return res[0]


if __name__ == "__main__":

    initial_source = Source(data_source="initial inserts", date_obtained=date.today())
    org_type_list = [
        "Corporation",
        "Government",
        "Charity",
        "Professional Association",
        "Political Party",
        "Unclassified"
    ]
    sector_list = ["Government"]
    org_list = {
        "Federal Government of Canada": {"type": "Government", "sector": "Government"}
    }

    db_host = "localhost"
    db_name = "lq_test"
    db_user = "test_user"
    db_pw = "changethis"
    schema_name = "lf_mockup"

    motor = create_engine(
        f"postgresql+psycopg2://{db_user}:{db_pw}@localhost/{db_name}", echo=True
    )

    session = Session(motor)
    for tn in org_type_list:

        stat = select(OrganizationType.id).where(
            OrganizationType.match_name == create_match_name(tn)
        )
        res = session.exec(stat).first()

        if res is None:
            ot = OrganizationType(display_name=tn, match_name=create_match_name(tn))
            session.add(ot)

    session.commit()
    session.close()

    session = Session(motor)
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
    session.close()

    session = Session(motor)
    for on in org_list.keys():
        stat = select(Organization.id).where(
            Organization.match_name == create_match_name(on)
        )
        res = session.exec(stat).first()

        if res is None:
            src_id = ensure_source(motor, initial_source)

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
