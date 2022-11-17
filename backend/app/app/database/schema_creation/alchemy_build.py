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

    # Information source/Reference
    source = sa.Table('source',
                      metadata,
                      sa.Column('id', sa.BigInteger, sa.Identity(), primary_key=True),
                      sa.Column('date_obtained', sa.Date, nullable=False),
                      sa.Column('data_source', sa.Text, nullable=False),
                      sa.Column('misc_data', pg.JSONB),
                      )

    # Individual humans
    person = sa.Table('person',
                      metadata,
                      sa.Column('id', sa.BigInteger, sa.Identity(), primary_key=True),
                      sa.Column('display_name', sa.Text, unique=True, nullable=False),
                      sa.Column('match_name', sa.Text, unique=True, nullable=False),
                      sa.Column('source', sa.BigInteger, sa.ForeignKey('source.id'), nullable=False)
                      )

    # Standard non-overlapping sector/topic
    sector = sa.Table('sector',
                      metadata,
                      sa.Column('id', sa.Integer, sa.Identity(), primary_key=True),
                      sa.Column('display_name', sa.Text, unique=True, nullable=False),
                      sa.Column('match_name', sa.Text, unique=True, nullable=False),
                      )

    # Corporations, government, lobbying groups, special interests, etc.
    org_type = sa.Table('organization_type',
                        metadata,
                        sa.Column('id', sa.Integer, sa.Identity(), primary_key=True),
                        sa.Column('display_name', sa.Text, unique=True, nullable=False),
                        sa.Column('match_name', sa.Text, unique=True, nullable=False),
                        )

    # Organizations (corporations, government, cabinet, associations, etc.)
    organization = sa.Table('organization',
                            metadata,
                            sa.Column('id', sa.BigInteger, sa.Identity(), primary_key=True),
                            sa.Column('display_name', sa.Text, unique=True, nullable=False),
                            sa.Column('match_name', sa.Text, unique=True, nullable=False),
                            sa.Column('organization_type', sa.Integer, sa.ForeignKey('organization_type.id'), nullable=False),
                            sa.Column('parent_organization', sa.BigInteger, sa.ForeignKey('organization.id')),
                            sa.Column('sector', sa.Integer, sa.ForeignKey('sector.id'), nullable=False),
                            sa.Column('source', sa.BigInteger, sa.ForeignKey('source.id'), nullable=False),
                            sa.Column('misc_data', pg.JSONB)
                            )

    # People belonging to organizations
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

    # Person to Person (comms log)
    communications = sa.Table('communications',
                              metadata,
                              sa.Column('id', sa.BigInteger, sa.Identity(), primary_key=True),
                              sa.Column('party_1', sa.BigInteger, sa.ForeignKey('person.id'), nullable=False),
                              sa.Column('party_2', sa.BigInteger, sa.ForeignKey('person.id'), nullable=False),
                              sa.Column('date', sa.Date, nullable=False),
                              sa.Column('sector', sa.Integer, sa.ForeignKey('sector.id')),
                              sa.Column('source', sa.BigInteger, sa.ForeignKey('source.id'), nullable=False)
                              )

    # Monetary exchange (future use)
    funding = sa.Table('funding',
                       metadata,
                       sa.Column('id', sa.BigInteger, sa.Identity(), primary_key=True),
                       sa.Column('party_1', sa.BigInteger, sa.ForeignKey('organization.id'), nullable=False),
                       sa.Column('party_2', sa.BigInteger, sa.ForeignKey('organization.id'), nullable=False),
                       sa.Column('amount', sa.Integer, nullable=False),
                       sa.Column('start_date', sa.Date),
                       sa.Column('end_date', sa.Date),
                       sa.Column('source', sa.BigInteger, sa.ForeignKey('source.id'), nullable=False)
                       )

    # Details of the corporation (an organization of type corporation)
    corporation_info = sa.Table('corporate_info',
                                metadata,
                                sa.Column('id', sa.BigInteger, sa.Identity(), primary_key=True),
                                sa.Column('organization', sa.BigInteger, sa.ForeignKey('organization.id'), nullable=False, unique=True),
                                sa.Column('corporate_number', sa.BigInteger, nullable=False, unique=True),
                                sa.Column('stock_ticker', sa.String(10), unique=True),
                                sa.Column('source', sa.BigInteger, sa.ForeignKey('source.id'), nullable=False))

    metadata.create_all(sa_engine)

print("done")

