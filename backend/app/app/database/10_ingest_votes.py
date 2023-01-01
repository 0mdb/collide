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
data_dir_votes_summary = os.path.join("votes", "summary")
data_dir_votes_detailed = os.path.join("votes", "detail")

# Folder creation, directories
curr_dir_name = os.path.dirname(__file__)

absolute_project_path = None
for i in pathlib.Path(curr_dir_name).parents:
    if i.name == project_name:
        absolute_project_path = i.absolute()
        break

summary_dir = os.path.join(absolute_project_path, data_dir, data_dir_votes_summary)
detail_dir = os.path.join(absolute_project_path, data_dir, data_dir_votes_detailed)

# Add source for vote summary and detailed
vote_summary_meta = glob.glob(summary_dir + "/meta.csv")
summary_meta_df = pd.read_csv(vote_summary_meta[0])

vote_detail_meta = glob.glob(detail_dir + "/meta.csv")
detail_meta_df = pd.read_csv(vote_detail_meta[0])

sum_file_lst = glob.glob(summary_dir + "/*.csv")
sum_file_lst = [x for x in sum_file_lst if os.path.basename(x) != "meta.csv"]
sum_file_lst_base = [os.path.basename(x) for x in sum_file_lst]

det_file_lst = glob.glob(detail_dir + "/*.xml")
det_file_lst_base = [os.path.basename(x) for x in det_file_lst]

# TODO: Change from debug when ready
session = cf.create_session()
summary_src_obj = cf.add_sources(session,
                                 [{
                                     "data_source": summary_meta_df["source_name"].to_list()[0],
                                     "date_obtained": datetime.datetime.fromisoformat(summary_meta_df["date_scraped"].to_list()[0]).date(),
                                     "misc_data": {"filenames": sum_file_lst_base,
                                                   "url": summary_meta_df["source_url"].to_list()[0]}
                                 }])[0]
detail_src_obj = cf.add_sources(session,
                                [{
                                    "data_source": detail_meta_df["source_name"].to_list()[0],
                                    "date_obtained": datetime.datetime.fromisoformat(detail_meta_df["date_scraped"].to_list()[0]).date(),
                                    "misc_data": {"filenames": det_file_lst_base,
                                                  "url": detail_meta_df["source_url"].to_list()[0]}
                                }])[0]

# Construct list of Vote entries
# Vote overview info
df = pd.DataFrame()
for each_csv in sum_file_lst:
    df = df.append(pd.read_csv(each_csv))

parl = df["Parliament"].to_list()
parl_session = df["Session"].to_list()
vote_no = df["Vote Number"].to_list()
dates = df["Date"].to_list()
desc = df["Vote Subject"].to_list()
vote_res = df["Vote Result"].to_list()
yeas = df["Yeas"].to_list()
nays = df["Nays"].to_list()
pairs = df["Paired"].to_list()
bill_no = df["Bill Number"].to_list()

vote_ensemble = []
print(f"Number of votes to ingest: {len(vote_no)}")
for idx, each_vote_no in enumerate(vote_no):
    vote_ensemble.append({
        "parliament": parl[idx],
        "parliament_session": parl_session[idx],
        "date_held": dates[idx],
        "vote_number": each_vote_no,
        "description": desc[idx],
        "yeas": yeas[idx],
        "nays": nays[idx],
        "paired": pairs[idx],
        "result": vote_res[idx],
        "bill_name": bill_no[idx],
        "source_id": summary_src_obj.id
    })

vote_objs = cf.add_votes(session, vote_ensemble)

# Construct list of VoteIndividual entries
# Call cf.add_vote_individual
#
# with open(bills_json[0], encoding="utf-8") as f:
#     data = f.read()
#     structure = json.loads(data)
#
# bills_df = pd.json_normalize(structure)
#
# bill_name = bills_df["NumberCode"].to_list()
# parl = bills_df["ParliamentNumber"].to_list()
# parl_session = bills_df["SessionNumber"].to_list()
# desc = bills_df["LongTitleEn"].to_list()
# house_bool = bills_df["IsHouseBill"].to_list()
# senate_bool = bills_df["IsSenateBill"].to_list()
# first_house_read_date = bills_df["PassedHouseFirstReadingDateTime"].to_list()
# second_house_read_date = bills_df["PassedHouseSecondReadingDateTime"].to_list()
# third_house_read_date = bills_df["PassedHouseThirdReadingDateTime"].to_list()
# first_senate_read_date = bills_df["PassedSenateFirstReadingDateTime"].to_list()
# second_senate_read_date = bills_df["PassedSenateSecondReadingDateTime"].to_list()
# third_senate_read_date = bills_df["PassedSenateThirdReadingDateTime"].to_list()
# royal_assent_date = bills_df["ReceivedRoyalAssentDateTime"].to_list()
#
# print(f"Expected entry count: {len(bill_name)}")
#
# bill_lst = []
# for idx, every_bill in enumerate(bill_name):
#     bill_lst.append({"bill_name": every_bill,
#                      "parliament": parl[idx],
#                      "parliament_session": parl_session[idx],
#                      "description": desc[idx],
#                      "is_house_bill": house_bool[idx],
#                      "is_senate_bill": senate_bool[idx],
#                      "first_house_read_date": first_house_read_date[idx],
#                      "second_house_read_date": second_house_read_date[idx],
#                      "third_house_read_date": third_house_read_date[idx],
#                      "first_senate_read_date": first_senate_read_date[idx],
#                      "second_senate_read_date": second_senate_read_date[idx],
#                      "third_senate_read_date": third_senate_read_date[idx],
#                      "royal_assent_date": royal_assent_date[idx],
#                      "source_id": src_obj.id})
#
# bills_objs = cf.add_bills(session, bill_lst)

session.close()
print("END")
