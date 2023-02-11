import glob
import os
import pandas as pd
import common_func as cf
from DirectoryHandler import DirectoryHandler
import datetime


def insert_vote_voteindividual(debug_status, cutoff_dt):
    print("\tstarted bill votes")

    # Preamble, folder locations
    dh_votes = DirectoryHandler("votes summary")
    dh_votes.load_meta_file()

    dh_votesindividual = DirectoryHandler("votes detail")
    dh_votesindividual.load_meta_file()

    sum_file_lst = glob.glob(dh_votes.path_of_interest + "/*.csv")
    sum_file_lst = [x for x in sum_file_lst if os.path.basename(x) != "meta.csv"]

    det_file_lst_raw = glob.glob(dh_votesindividual.path_of_interest + "/*.xml")
    det_file_lst = [x for x in det_file_lst_raw if os.path.getsize(x) > 5000]

    # sum_file_lst_base = [os.path.basename(x) for x in sum_file_lst]
    # det_file_lst_base = [os.path.basename(x) for x in det_file_lst]

    session = cf.create_session(debug=debug_status)

    # Grab sources (vote summary)
    dh_votes.load_meta_file()
    summary_src_obj = cf.add_sources(session, [{"data_source": dh_votes.source_name,
                                                "date_obtained": dh_votes.source_age,
                                                "misc_data": dh_votes.source_misc}])[0]

    dh_votesindividual.load_meta_file()
    detail_src_obj = cf.add_sources(session, [{"data_source": dh_votesindividual.source_name,
                                               "date_obtained": dh_votesindividual.source_age,
                                               "misc_data": dh_votesindividual.source_misc}])[0]

    # Construct list of Vote entries
    # Vote overview info
    df = pd.DataFrame()
    for each_csv in sum_file_lst:
        df = df.append(pd.read_csv(each_csv))

    parl = df["Parliament"].to_list()
    parl_session = df["Session"].to_list()
    vote_no = df["Vote Number"].to_list()
    dates = df["Date"].to_list()  # not isoformat
    desc = df["Vote Subject"].to_list()
    vote_res = df["Vote Result"].to_list()
    yeas = df["Yeas"].to_list()
    nays = df["Nays"].to_list()
    pairs = df["Paired"].to_list()
    bill_no = df["Bill Number"].to_list()

    vote_ensemble = []
    print(f"\tNumber of votes to ingest: {len(vote_no)}")
    for idx, each_vote_no in enumerate(vote_no):
        if datetime.datetime.fromisoformat(dates[idx].split()[0]) > cutoff_dt:
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
    print(f"\tNumber of votes meeting threshold: {len(vote_ensemble)}")
    vote_objs = cf.add_votes(session, vote_ensemble)

    # Construct list of VoteIndividual entries
    # Call cf.add_vote_individual
    print(f"\tStarted xml concatenation (slow)")
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
    event_date = individual_votes_df["DecisionEventDateTime"].to_list()

    print(f"\tExpected IndVote entry count: {len(parl)}")

    ind_vote_lst = []
    for idx, parl_entry in enumerate(parl):
        print(f"\t\tLoop: {idx} of {len(parl)}")
        if datetime.datetime.fromisoformat(event_date[idx]) > cutoff_dt:
            ind_vote_lst.append({"parliament": parl[idx],
                                 "parliament_session": parl_session[idx],
                                 "vote_no": vote_no[idx],
                                 "first_name": first_name[idx],
                                 "last_name": last_name[idx],
                                 "yes_bool": yes_bool[idx],
                                 "no_bool": no_bool[idx],
                                 "pair_bool": pair_bool[idx],
                                 "source_id": detail_src_obj.id})

    print(f"\tIndVote meeting threshold: {len(ind_vote_lst)}")
    ind_vote_objs = cf.add_individual_votes(session, ind_vote_lst)

    session.close()
    print("\tcompleted bill votes")

