from sqlmodel import Session, create_engine
from parse_injest.utils import create_match_name
from schema_creation.sqlmodel_build import OrganizationType

if __name__ == "__main__":

    org_type_list = ['Corporation', 'Government', 'Charity', 'Professional Association']

    db_host = "localhost"
    db_name = "lq_test"
    db_user = "test_user"
    db_pw = "changethis"
    schema_name = "lf_mockup"

    engine = create_engine(f"postgresql+psycopg2://{db_user}:{db_pw}@localhost/{db_name}",  echo=True)

    session = Session(engine)

    for tn in org_type_list:
        ot = OrganizationType(display_name=tn, match_name=create_match_name(tn))
        session.add(ot)

    session.commit()
    session.close()

