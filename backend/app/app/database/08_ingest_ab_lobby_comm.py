import datetime
import os
import pathlib
from sqlmodel import Session, create_engine, select
from schema_creation.sqlmodel_build import (
    Source
)
from pathlib import Path

# Manually designate sources
# 2022-11-21

# date_obtained: date = Field(sa_column=sa.Column(sa.Date, nullable=False))
# data_source: str
# misc_data: dict = Field(default={}, sa_column=sa.Column(pg.JSONB))

# Preamble, folder locations
project_name = "app"  # collide\backend\app\app
data_dir = "data"
data_dir_ab = "prov_ab"

# Folder creation, directories
curr_dir_name = os.path.dirname(__file__)

absolute_project_path = None
for i in pathlib.Path(curr_dir_name).parents:
    if i.name == project_name:
        absolute_project_path = i.absolute()
        break

file_dir = os.path.join(absolute_project_path, data_dir, data_dir_ab)

# Insert source for lobbying website

manual_sources = [
    {"date_obtained": datetime.datetime.fromisoformat("2022-12-06T00:00:00+00:00"),
     "data_source": "Alberta Lobby Registry",
     "misc_data": {"filenames": ["lobby_comm_ab.csv"],
                   "url": "https://www.albertalobbyistregistry.ca/"}}
]

db_host = "localhost"
db_name = "lq_test"
db_user = "test_user"
db_pw = "changethis"
schema_name = "lf_mockup_2"

motor = create_engine(
    f"postgresql+psycopg2://{db_user}:{db_pw}@localhost/{db_name}", echo=True
)

session = Session(motor)

for each_dict in manual_sources:
    # Check if it already exists with same timestamp
    stat = select(Source.id).where(
        Source.data_source == each_dict.get("data_source")
    ).where(
        Source.date_obtained == each_dict.get("date_obtained"))
    res = session.exec(stat).all()

    if len(res) == 0:
        ot = Source(data_source=each_dict.get("data_source"),
                    date_obtained=each_dict.get("date_obtained"),
                    misc_data=each_dict.get("misc_data"))
        session.add(ot)
        session.commit()

session.close()

# Ingest csv

# Organization inserts from "Organization", "Client Name"
# Organization inserts from "Government Department Lobbied" and "Prescribed Provincial Entity Lobbied" (parent GoA)
# Person inserts from "Designated Filer" and "Lobbyists"
# OrganizationMembership inserts between filer/lobbyists and organization/client name
# CommsTopic inserts from "Subject Matter of Lobbying"
# CommunicationsP2O (new table?) inserts between filer/lobbyists with departments/entities
