# TODO: write ingestion of elections canada contributions
import glob
import os
import pathlib

import pandas as pd
from pydantic import BaseModel
from typing import List, Optional


class Transaction:

    def __init__(self, pol_ent, recip_f, recip_l, recip_party, fiscal_date, con_type, con_l, con_f, amt):
        self.pol_ent = pol_ent
        self.recip_f = recip_f
        self.recip_l = recip_l
        self.recip_party = recip_party
        self.fiscal_date = fiscal_date
        self.con_type = con_type
        self.con_l = con_l
        self.con_f = con_f
        self.amt = amt


class ElxCsv:
    # Collecting everything up front
    # Electoral District ignored as membership (not elected and otherwise captured as MP)

    def __init__(self, file_path):
        self.csv_path = file_path
        self.df = None
        self.transactions = None

        self.recip_ent_ppl = ["Candidates",
                              "Leadership contestants",
                              "Nomination contestants"]

        self.recip_ent_parties = ["Registered parties",
                                  "Registered associations"]

        self.contrib_ppl = ["Individuals"]
        self.contrib_corp = ["Corporations"]
        self.contrib_union = ["Trade unions"]
        self.contrib_assoc = ["Unincorporated Associations"]
        self.contrib_gov = ["Governments"]

    def load_csv(self):
        self.df = pd.read_csv(self.csv_path)

    def build_transactions(self):
        self.df["Political Entity"].to_list()
        self.df["Recipient last name"].to_list()
        self.df["Recipient first name"].to_list()
        self.df["Political Party of Recipient"].to_list()
        self.df["Fiscal/Election date"].to_list()

        self.df["Contributor type"].to_list()
        self.df["Contributor last name"].to_list()
        self.df["Contributor first name"].to_list()
        self.df["Monetary amount"].to_list()

        # TODO: fix this
        self.transactions = [Transaction(a["Political Entity"],
                                         a["Recipient last name"],
                                         a["Recipient first name"],
                                         a["Political Party of Recipient"],
                                         a["Fiscal/Election date"],
                                         a["Contributor type"],
                                         a["Contributor last name"],
                                         a["Contributor first name"],
                                         a["Monetary amount"]) for a in self.df.itertuples()]


# Preamble, folder locations
project_name = "app"  # collide\backend\app\app
data_dir = "data"
data_dir_contrib = "ecanada_contrib"

# Folder creation, directories
curr_dir_name = os.path.dirname(__file__)

absolute_project_path = None
for i in pathlib.Path(curr_dir_name).parents:
    if i.name == project_name:
        absolute_project_path = i.absolute()
        break

contrib_dir = os.path.join(absolute_project_path, data_dir, data_dir_contrib)

contrib_csv = glob.glob(contrib_dir + "/*od_cntrbtn_audt_e.csv")

if len(contrib_csv) > 1:
    raise RuntimeError("More than one csv detected.")

election_csv = ElxCsv(contrib_csv[0])
election_csv.load_csv()
election_csv.build_transactions()

print("stop")
