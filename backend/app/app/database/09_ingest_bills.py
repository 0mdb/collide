import datetime
import glob
import os
import pathlib
import pandas as pd
import common_func as cf
import json
from parse_injest.utils import create_match_name
from schema_creation.sqlmodel_build import (
    LegStage
)
from sqlmodel import select


# Preamble, folder locations
project_name = "app"  # collide\backend\app\app
data_dir = "data"
data_dir_bills = "bills"
data_dir_summary = "summary"

# Folder creation, directories
curr_dir_name = os.path.dirname(__file__)

absolute_project_path = None
for i in pathlib.Path(curr_dir_name).parents:
    if i.name == project_name:
        absolute_project_path = i.absolute()
        break

summary_dir = os.path.join(absolute_project_path, data_dir, data_dir_bills, data_dir_summary)

# Add source for Bill entries
bills_meta = glob.glob(summary_dir + "/meta.csv")
meta_df = pd.read_csv(bills_meta[0])
date_scraped = meta_df["date_scraped"].to_list()[0]
source_name = meta_df["source_name"].to_list()[0]
source_url = meta_df["source_url"].to_list()[0]

bills_json = glob.glob(summary_dir + "/*.json")

if len(bills_json) > 1:
    raise RuntimeError("More than one json detected.")

# TODO: Change from debug when ready
session = cf.create_session()
src_obj = cf.add_sources(session,
                          [{
                              "data_source": source_name,
                              "date_obtained": datetime.datetime.fromisoformat(date_scraped).date(),
                              "misc_data": {"filenames": [os.path.basename(bills_json[0])],
                                            "url": source_url}
                          }])[0]

# Populate LegStage table with standard stages
leg_stages = [
    "House Reading First",
    "House Reading Second",
    "House Reading Third",
    "Senate Reading First",
    "Senate Reading Second",
    "Senate Reading Third",
    "Royal Assent"
]

for each_stage in leg_stages:
    # Check if it already exists
    stat = select(LegStage).where(
        LegStage.match_name == create_match_name(each_stage)
    )
    res = session.exec(stat).all()

    if len(res) == 0:
        new_stage = LegStage(display_name=each_stage,
                             match_name=create_match_name(each_stage))

        session.add(new_stage)
        session.commit()
    else:
        print(f"LegStage {each_stage} already exists")

# Construct list of bills
with open(bills_json[0], encoding="utf-8") as f:
    data = f.read()
    structure = json.loads(data)

bills_df = pd.json_normalize(structure)

bill_name = bills_df["NumberCode"].to_list()
parl = bills_df["ParliamentNumber"].to_list()
parl_sess = bills_df["SessionNumber"].to_list()
desc = bills_df["LongTitleEn"].to_list()
house_bool = bills_df["IsHouseBill"].to_list()
senate_bool = bills_df["IsSenateBill"].to_list()
first_house_read_date = bills_df["PassedHouseFirstReadingDateTime"].to_list()
second_house_read_date = bills_df["PassedHouseSecondReadingDateTime"].to_list()
third_house_read_date = bills_df["PassedHouseThirdReadingDateTime"].to_list()
first_senate_read_date = bills_df["PassedSenateFirstReadingDateTime"].to_list()
second_senate_read_date = bills_df["PassedSenateSecondReadingDateTime"].to_list()
third_senate_read_date = bills_df["PassedSenateThirdReadingDateTime"].to_list()
royal_assent_date = bills_df["ReceivedRoyalAssentDateTime"].to_list()

print(f"Expected entry count: {len(bill_name)}")

bill_lst = []
for idx, every_bill in enumerate(bill_name):
    bill_lst.append({"bill_name": every_bill,
                     "parliament": parl[idx],
                     "parliament_session": parl_sess[idx],
                     "description": desc[idx],
                     "is_house_bill": house_bool[idx],
                     "is_senate_bill": senate_bool[idx],
                     "first_house_read_date": first_house_read_date[idx],
                     "second_house_read_date": second_house_read_date[idx],
                     "third_house_read_date": third_house_read_date[idx],
                     "first_senate_read_date": first_senate_read_date[idx],
                     "second_senate_read_date": second_senate_read_date[idx],
                     "third_senate_read_date": third_senate_read_date[idx],
                     "royal_assent_date": royal_assent_date[idx],
                     "source_id": src_obj.id})

bills_objs = cf.add_bills(session, bill_lst)

# TODO: Detect differences between text (function)

session.close()
print("END")
