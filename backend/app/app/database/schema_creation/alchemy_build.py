import sqlalchemy as sa
import sqlalchemy.dialects.postgresql as pg

db_host = "localhost"
db_name = "lq_test"
db_user = "test_user"
db_pw = "changethis"
schema_name = "lf_mockup"

drop_tables = False


sa_engine = sa.engine.create_engine(f"postgresql+psycopg2://{db_user}:{db_pw}@localhost/{db_name}")

inspection = sa.inspect(sa_engine)
schemas = inspection.get_schema_names()

connection = sa_engine.connect()
metadata = sa.MetaData(schema='lf_mockup')
metadata.reflect(sa_engine, schema='lf_mockup')
if drop_tables:
    metadata.drop_all(sa_engine)
    #sa_engine.dispose()
    #metadata.reflect(sa_engine, schema='lf_mockup')
else:

    source = sa.Table('source',
                      metadata,
                      sa.Column('id', sa.BigInteger, sa.Identity(), primary_key=True),
                      sa.Column('date_obtained', sa.Date, nullable=False),
                      sa.Column('data_source', sa.Text, nullable=False),
                      sa.Column('misc_data', pg.JSONB),
                      )


    person = sa.Table('person',
                      metadata,
                      sa.Column('id', sa.BigInteger, sa.Identity(), primary_key=True),
                      sa.Column('display_name', sa.Text, unique=True),
                      sa.Column('match_name', sa.Text, unique=True),
                      sa.Column('source', sa.BigInteger, sa.ForeignKey('source.id'))
                      )

    sector = sa.Table('sector',
                      metadata,
                      sa.Column('id', sa.Integer, sa.Identity(), primary_key=True),
                      sa.Column('display_name', sa.Text, unique=True),
                      sa.Column('match_name', sa.Text, unique=True),
                      )

    org_type = sa.Table('organization_type',
                        metadata,
                        sa.Column('id', sa.Integer, sa.Identity(), primary_key=True),
                        sa.Column('display_name', sa.Text, unique=True),
                        sa.Column('match_name', sa.Text, unique=True),
                        )

    organization = sa.Table('organization',
                            metadata,
                            sa.Column('id', sa.BigInteger, sa.Identity(), primary_key=True),
                            sa.Column('display_name', sa.Text, unique=True),
                            sa.Column('match_name', sa.Text, unique=True),
                            sa.Column('organization_type', sa.Integer, sa.ForeignKey('organization_type.id'), nullable=False),
                            sa.Column('parent_organization', sa.BigInteger, sa.ForeignKey('organization.id')),
                            sa.Column('sector', sa.Integer, sa.ForeignKey('sector.id')),
                            sa.Column('source', sa.BigInteger, sa.ForeignKey('source.id'), nullable=False),
                            sa.Column('misc_data', pg.JSONB)
                            )

    organization_membership = sa.Table('organization_membership',
                                       metadata,
                                       sa.Column('id', sa.BigInteger, sa.Identity(), primary_key=True),
                                       sa.Column('person', sa.BigInteger, sa.ForeignKey('person.id'), nullable=False),
                                       sa.Column('organization', sa.BigInteger, sa.ForeignKey('organization.id'),
                                                 nullable=False),
                                       sa.Column('source', sa.BigInteger, sa.ForeignKey('source.id'), nullable=False),
                                       sa.Column('start_date', sa.Date),
                                       sa.Column('end_date', sa.Date)
                                       )

    communications = sa.Table('communications',
                              metadata,
                              sa.Column('id', sa.BigInteger, sa.Identity(), primary_key=True),
                              sa.Column('party_1', sa.BigInteger, sa.ForeignKey('person.id'), nullable=False),
                              sa.Column('party_2', sa.BigInteger, sa.ForeignKey('person.id'), nullable=False),
                              sa.Column('date', sa.Date),
                              sa.Column('sector', sa.Integer, sa.ForeignKey('sector.id')),
                              sa.Column('source', sa.BigInteger, sa.ForeignKey('source.id'), nullable=False)
                              )

    funding = sa.Table('funding',
                       metadata,
                       sa.Column('id', sa.BigInteger, sa.Identity(), primary_key=True),
                       sa.Column('party_1', sa.BigInteger, sa.ForeignKey('organization.id'), nullable=False),
                       sa.Column('party_2', sa.BigInteger, sa.ForeignKey('organization.id'), nullable=False),
                       sa.Column('start_date', sa.Date),
                       sa.Column('end_date', sa.Date),
                       sa.Column('source', sa.BigInteger, sa.ForeignKey('source.id'), nullable=False)
                       )

    corporation_info = sa.Table('corporate_info',
                                metadata,
                                sa.Column('id', sa.BigInteger, sa.Identity(), primary_key=True),
                                sa.Column('organization', sa.BigInteger, sa.ForeignKey('organization.id'), nullable=False),
                                sa.Column('corporate_number', sa.BigInteger),
                                sa.Column('source', sa.BigInteger, sa.ForeignKey('source.id'), nullable=False))


    metadata.create_all(sa_engine)

print("done")

