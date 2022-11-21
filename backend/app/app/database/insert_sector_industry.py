import os
import pathlib
import pandas as pd
import glob
from sqlmodel import Session, create_engine, select, engine
from schema_creation.sqlmodel_build import (
    SectorIndustry
)
from parse_injest.utils import create_match_name

# https://ised-isde.canada.ca/site/corporations-canada/en/data-services#1

# Preamble, folder locations
project_name = "app"  # collide\backend\app\app
data_dir = "data"
data_dir_corp_tsx = "corp_tsx"

# Folder creation, directories
curr_dir_name = os.path.dirname(__file__)

absolute_project_path = None
for i in pathlib.Path(curr_dir_name).parents:
    if i.name == project_name:
        absolute_project_path = i.absolute()
        break

file_dir = os.path.join(absolute_project_path, data_dir, data_dir_corp_tsx)
tsx_csv = glob.glob("*tsx*.csv")

if len(tsx_csv) > 0:
    raise RuntimeError("More than one csv detected.")

df = pd.read_csv(tsx_csv[0])
sectors = df["sector"].to_list()
industries = df["industry"].to_list()

db_host = "localhost"
db_name = "lq_test"
db_user = "test_user"
db_pw = "changethis"
schema_name = "lf_mockup"

motor = create_engine(
    f"postgresql+psycopg2://{db_user}:{db_pw}@localhost/{db_name}", echo=True
)

session = Session(motor)
for idx, itm in enumerate(sectors):
    # Check if it already exists
    stat = select(SectorIndustry.id).where(
        SectorIndustry.sector_match_name == create_match_name(sectors[idx]) and
        SectorIndustry.industry_match_name == create_match_name(industries[idx])
    )
    res = session.exec(stat).all()

    if len(res) == 0:
        ot = SectorIndustry(sector_display_name=sectors[idx],
                            sector_match_name=create_match_name(sectors[idx]),
                            industry_display_name=industries[idx],
                            industry_match_name=create_match_name(industries[idx]))
        session.add(ot)

session.commit()
session.close()
