import os
import pathlib
import pandas as pd
import glob
from sqlmodel import Session, create_engine, select, engine
from schema_creation.sqlmodel_build import (
    CommsTopic
)
from parse_injest.utils import create_match_name

# Preamble, folder locations
project_name = "app"  # collide\backend\app\app
data_dir = "data"
data_dir_reg = "lobby_regs"
data_dir_comm = "lobby_comms"

# Folder creation, directories
curr_dir_name = os.path.dirname(__file__)

absolute_project_path = None
for i in pathlib.Path(curr_dir_name).parents:
    if i.name == project_name:
        absolute_project_path = i.absolute()
        break

file_dir = os.path.join(absolute_project_path, data_dir, data_dir_reg)
sub_csv_1 = glob.glob(file_dir + "/*SubjectMattersExport.csv")

file_dir = os.path.join(absolute_project_path, data_dir, data_dir_comm)
sub_csv_2 = glob.glob(file_dir + "/*SubjectMattersExport.csv")

sub_csv = sub_csv_1 + sub_csv_2

if len(sub_csv) > 2:
    raise RuntimeError("More than expected two csv detected.")

db_host = "localhost"
db_name = "lq_test"
db_user = "test_user"
db_pw = "changethis"
schema_name = "lf_mockup"

motor = create_engine(
        f"postgresql+psycopg2://{db_user}:{db_pw}@localhost/{db_name}", echo=True
)

session = Session(motor)

for each_file in sub_csv:
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
