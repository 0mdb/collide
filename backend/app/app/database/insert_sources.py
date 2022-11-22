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
data_dir_members = "members_xml"
data_dir_cabinet = "cabinet_xml"
data_dir_boards = "corp_board"

# Folder creation, directories
curr_dir_name = os.path.dirname(__file__)

absolute_project_path = None
for i in pathlib.Path(curr_dir_name).parents:
    if i.name == project_name:
        absolute_project_path = i.absolute()
        break

our_commons_file_list = []
file_dir = os.path.join(absolute_project_path, data_dir, data_dir_members)

for path in Path(file_dir).rglob("*"):
    if os.path.isfile(path):
        our_commons_file_list.append(os.path.basename(path))

file_dir = os.path.join(absolute_project_path, data_dir, data_dir_cabinet)

for path in Path(file_dir).rglob("*"):
    if os.path.isfile(path):
        our_commons_file_list.append(os.path.basename(path))

file_dir = os.path.join(absolute_project_path, data_dir, data_dir_boards)

corp_directors_list = []
for path in Path(file_dir).glob("*.csv"):
    corp_directors_list.append(os.path.basename(path))

manual_sources = [
    {"date_obtained": datetime.datetime.fromisoformat("2022-11-19T23:17:00+00:00"),  # UTC ISO
     "data_source": "Office of the Commissioner of Lobbying of Canada, Lobbying Registrations",
     "misc_data": {"filenames": ["Registration_BeneficiariesExport.csv",
                                 "Registration_CommunicationTechniquesExport.csv",
                                 "Registration_ConsultantLobbyistsExport.csv",
                                 "Registration_GovernmentInstExport.csv",
                                 "Registration_GovtFundingExport.csv",
                                 "Registration_InHouseLobbyistsExport.csv",
                                 "Registration_ManuallyEntered_GovernmentInstExport.csv",
                                 "Registration_PrimaryExport.csv",
                                 "Registration_PublicOfficeExport.csv",
                                 "Registration_SubjectMatterDetailsExport.csv",
                                 "Registration_SubjectMattersExport.csv"],
                   "url": "https://lobbycanada.gc.ca/en/open-data/"}},
    {"date_obtained": datetime.datetime.fromisoformat("2022-11-19T23:17:00+00:00"),
     "data_source": "Office of the Commissioner of Lobbying of Canada, Monthly Communication Reports",
     "misc_data": {"filenames": ["Communication_DpohExport.csv",
                                 "Communication_PrimaryExport.csv",
                                 "Communication_SubjectMattersExport.csv"],
                   "url": "https://lobbycanada.gc.ca/en/open-data/"}},
    {"date_obtained": datetime.datetime.fromisoformat("2022-11-13T21:36:00+00:00"),
     "data_source": "Wikipedia, S&P/TSX Composite Index",
     "misc_data": {"filenames": ["20210920_comp_index_tsx.csv"],
                   "url": "https://en.wikipedia.org/wiki/S%26P/TSX_Composite_Index"}},
    {"date_obtained": datetime.datetime.fromisoformat("2022-11-11T00:00:00+00:00"),
     "data_source": "Innovation, Science and Economic Development Canada, Corporations Canada Search",
     "misc_data": {"filenames": ["20221111_corp_no_listing.csv"],
                   "url": "https://www.ic.gc.ca/app/scr/cc/CorporationsCanada/fdrlCrpSrch.html"}},
    {"date_obtained": datetime.datetime.fromisoformat("2022-11-11T00:00:00+00:00"),
     "data_source": "Innovation, Science and Economic Development Canada, Corporations Canada API",
     "misc_data": {"filenames": corp_directors_list,
                   "url": "https://ised-isde.canada.ca/site/corporations-canada/en/accessing-federal-corporation-json-datasets"}},
    {"date_obtained": datetime.datetime.fromisoformat("2022-11-13T21:36:00+00:00"),
     "data_source": "House of Commons Canada",
     "misc_data": {"filenames": our_commons_file_list,
                   "url": "https://www.ourcommons.ca/members/en"}}
]

db_host = "localhost"
db_name = "lq_test"
db_user = "test_user"
db_pw = "changethis"
schema_name = "lf_mockup"

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
