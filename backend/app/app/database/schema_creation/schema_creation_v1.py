import psycopg2

db_host = "localhost"
db_name = "test_db"
db_user = "postgres"
db_pw = "1212"

schema_name = "lf_mockup_v1"
drop_schema = True

conn = psycopg2.connect("dbname={} user={} password={} host={}".format(db_name, db_user, db_pw, db_host))
cur = conn.cursor()

if drop_schema:
    cur.execute("DROP SCHEMA IF EXISTS {} CASCADE;".format(schema_name))
    cur.execute("CREATE SCHEMA {};".format(schema_name))

source_table = (f"CREATE TABLE IF NOT EXISTS {schema_name}.source(id bigserial UNIQUE PRIMARY KEY NOT NULL, "
                f"date_obtained date, "
                f"data_source text);")
cur.execute(source_table)
conn.commit()

sector_table = (f"CREATE TABLE IF NOT EXISTS {schema_name}.sector(id bigserial UNIQUE PRIMARY KEY NOT NULL, "
                f"description text);")
cur.execute(sector_table)
conn.commit()

person_table = (f"CREATE TABLE IF NOT EXISTS {schema_name}.person(id bigserial unique primary key not null, "
                f"name text not null unique, "
                # f"affiliations json,"
                # f"affiliation_sources json);
                f"source integer references {schema_name}.source(id));")
cur.execute(person_table)
conn.commit()

relationship_type_table = (
    f"CREATE TABLE IF NOT EXISTS {schema_name}.relationship_type(id bigserial UNIQUE PRIMARY KEY NOT NULL, "
    f"description text NOT NULL);")
cur.execute(relationship_type_table)
conn.commit()

party_type_table = (f"CREATE TABLE IF NOT EXISTS {schema_name}.party_type(id bigserial UNIQUE PRIMARY KEY NOT NULL, "
                    f"description text);")
cur.execute(party_type_table)
conn.commit()

relationship_table = (
    f"CREATE TABLE IF NOT EXISTS {schema_name}.relationship(id bigserial UNIQUE PRIMARY KEY NOT NULL, "
    f"party_1 integer, "
    f"party_1_type integer references {schema_name}.party_type(id),"
    f"party_2 integer, "
    f"party_2_type integer references {schema_name}.party_type(id), "
    f"relation_type integer references {schema_name}.relationship_type(id), "
    f"sector integer references {schema_name}.sector(id), "
    f"source integer references {schema_name}.source(id));")
cur.execute(relationship_table)
conn.commit()

organization_type_table = (
    f"CREATE TABLE IF NOT EXISTS {schema_name}.organization_type(id bigserial UNIQUE PRIMARY KEY NOT NULL, "
    f"description text);")
cur.execute(organization_type_table)
conn.commit()

organization_table = (
    f"CREATE TABLE IF NOT EXISTS {schema_name}.organization(id bigserial UNIQUE PRIMARY KEY NOT NULL, "
    f"name text NOT NULL, "
    f"organization_type integer references {schema_name}.organization_type(id), "
    f"parent_org integer, "
    f"source integer references {schema_name}.source(id));")
cur.execute(organization_table)

conn.commit()

sql_insert = (
    f"INSERT INTO {schema_name}.relationship_type(description) VALUES ('COMMUNICATIONS'), ('MEMBER_OR_EMPLOYEE'), ('FUNDING');")
cur.execute(sql_insert)

sql_insert = (
    f"INSERT INTO {schema_name}.organization_type (description) VALUES ('CORPORATION'), ('GOVERNMENT'), ('LOBBY_GROUP'), ('NOT_FOR_PROFIT');")
cur.execute(sql_insert)

sql_insert = (f"INSERT INTO {schema_name}.party_type (description) VALUES ('ORGANIZATION'), ('PERSON');")
cur.execute(sql_insert)

conn.commit()
cur.close()
conn.close()
