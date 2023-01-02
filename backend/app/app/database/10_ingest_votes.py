import datetime
import glob
import os
import pathlib
import pandas as pd
import common_func as cf

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
individual_votes_df = pd.DataFrame()
for each_xml in det_file_lst:
    individual_votes_df = pd.concat([individual_votes_df, pd.read_xml(each_xml)], axis=0, ignore_index=True)

parl = individual_votes_df["ParliamentNumber"].to_list()
parl_session = individual_votes_df["SessionNumber"].to_list()
vote_no = individual_votes_df["DecisionDivisionNumber"].to_list()
first_name = individual_votes_df["PersonOfficialFirstName"].to_list()
last_name = individual_votes_df["PersonOfficialLastName"].to_list()
yes_bool = individual_votes_df["IsVoteYea"].to_list()
no_bool = individual_votes_df["IsVoteNay"].to_list()
pair_bool = individual_votes_df["IsVotePaired"].to_list()

print(f"Expected IndVote entry count: {len(parl)}")

ind_vote_lst = []
for idx, parl_entry in enumerate(parl):
    print(f"Loop: {idx} of {len(parl)}")
    ind_vote_lst.append({"parliament": parl[idx],
                         "parliament_session": parl_session[idx],
                         "vote_no": vote_no[idx],
                         "first_name": first_name[idx],
                         "last_name": last_name[idx],
                         "yes_bool": yes_bool[idx],
                         "no_bool": no_bool[idx],
                         "pair_bool": pair_bool[idx],
                         "source_id": detail_src_obj.id})

bills_objs = cf.add_individual_votes(session, ind_vote_lst)

session.close()
print("END")

# TODO: compare yea/nay/pair sums from completed VoteIndividual table vs Vote table totals when complete
