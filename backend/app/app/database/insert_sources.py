import os
import pathlib
import pandas as pd
import glob
from sqlmodel import Session, create_engine, select, engine
from schema_creation.sqlmodel_build import (
    Source
)
from parse_injest.utils import create_match_name


# Manually designate sources
# 2022-11-21

# date_obtained: date = Field(sa_column=sa.Column(sa.Date, nullable=False))
# data_source: str
# misc_data: dict = Field(default={}, sa_column=sa.Column(pg.JSONB))

manual_sources = [
    {"date_obtained": "2022-11-19T23:17:00+00:00",  # UTC ISO
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
    {"date_obtained": "2022-11-19T23:17:00+00:00",
     "data_source": "Office of the Commissioner of Lobbying of Canada, Monthly Communication Reports",
     "misc_data": {"filenames": ["Communication_DpohExport.csv",
                                 "Communication_PrimaryExport.csv",
                                 "Communication_SubjectMattersExport.csv"],
                   "url": "https://lobbycanada.gc.ca/en/open-data/"}},
    {"date_obtained": "2022-11-13T21:36:00+00:00",
     "data_source": "Wikipedia, S&P/TSX Composite Index",
     "misc_data": {"filenames": ["20210920_comp_index_tsx.csv"],
                   "url": "https://en.wikipedia.org/wiki/S%26P/TSX_Composite_Index"}},

    # TODO: I am here
    {"date_obtained": "xx",
     "data_source": "Corporate Numbers Source??",
     "misc_data": {"filenames": [""],
                   "url": ""}},
    {"date_obtained": "xx",
     "data_source": "Corporate Boards Source??",
     "misc_data": {"filenames": [""],
                   "url": ""}},
    {"date_obtained": "xx",
     "data_source": "Members XML Source??",
     "misc_data": {"filenames": [""],
                   "url": ""}},
    {"date_obtained": "xx",
     "data_source": "Cabinet XML Source??",
     "misc_data": {"filenames": [""],
                   "url": ""}},

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


df = pd.read_csv(each_file)
subs = df["SUBJ_MATTER_OBJET"].to_list()

for itm in subs:
    # Check if it already exists
    stat = select(CommsTopic.id).where(
        CommsTopic.match_name == create_match_name(itm)
    )
    res = session.exec(stat).all()

    if len(res) == 0:
        ot = CommsTopic(display_name=itm,
                        match_name=create_match_name(itm))
        session.add(ot)

session.commit()
session.close()
