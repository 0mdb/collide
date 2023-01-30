from sqlmodel_build import meta, schema_name, FundingPersonPerson, FundingPersonOrg, Bill, Vote, BillDiff, LegStage, VoteIndividual
from sqlmodel import Session, create_engine


def create_everything():
    db_host = "localhost"
    db_name = "lq_test"
    db_user = "test_user"
    db_pw = "changethis"
    # schema_name = "lf_mockup"

    engine = create_engine(f"postgresql+psycopg2://{db_user}:{db_pw}@{db_host}/{db_name}", echo=True)
    meta.create_all(engine)


def add_tables(debug=True):
    if debug:
        db_host = "localhost"
        db_name = "lq_test"
        db_user = "test_user"
        db_pw = "changethis"
        schema_name = "lf_mockup_2"
    else:
        db_host = "192.168.0.10"
        db_name = "collide"
        db_user = "test_user"
        db_pw = "change_this"
        # schema_name = "lf_mockup_2"

    motor = create_engine(
        f"postgresql+psycopg2://{db_user}:{db_pw}@{db_host}/{db_name}", echo=False
    )

    session = Session(motor)

    # FundingPersonPerson.__table__.create(session.bind)
    # FundingPersonOrg.__table__.create(session.bind)

    # Bill.__table__.create(session.bind)
    # Vote.__table__.create(session.bind)
    # VoteIndividual.__table__.create(session.bind)
    # LegStage.__table__.create(session.bind)
    # BillDiff.__table__.create(session.bind)
