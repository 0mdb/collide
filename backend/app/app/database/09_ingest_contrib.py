# TODO: write ingestion of elections canada contributions
import glob
import os
import pathlib

import pandas as pd
from pydantic import BaseModel
from typing import List, Optional


class Transaction:

    def __init__(self, pol_ent, recip_f, recip_l, recip_party, fiscal_date, con_type, con_f, con_l, amt):
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
        self.df = pd.read_csv(self.csv_path, nrows=100)

    def build_transactions(self):
        pe = self.df["Political Entity"].to_list()
        rl = self.df["Recipient last name"].to_list()
        rf = self.df["Recipient first name"].to_list()
        p = self.df["Political Party of Recipient"].to_list()
        d = self.df["Fiscal/Election date"].to_list()

        ct = self.df["Contributor type"].to_list()
        cl = self.df["Contributor last name"].to_list()
        cf = self.df["Contributor first name"].to_list()
        amt = self.df["Monetary amount"].to_list()

        tsn = []
        for idx, each_pe in enumerate(pe):
            tsn.append(Transaction(str(pe[idx]),
                                   str(rf[idx]),
                                   str(rl[idx]),
                                   str(p[idx]),
                                   str(d[idx]),
                                   str(ct[idx]),
                                   str(cf[idx]),
                                   str(cl[idx]),
                                   abs(float(amt[idx]))))
        self.transactions = tsn


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

# TODO: Apply threshold for contribution amount ($500)
# TODO: Insert people to people fund transfers
# From Contributor type = contrib_ppl --> Recipient type = recip_ent_ppl (filter)
# CONTRIBUTOR: Retrieve id from People (exists) or create People entry w/ no memberships (new)
# RECIPIENT: Retrieve id from People (exists) or create People entry w/ "Political Party of Recipient" membership (new)
# Enter FundingPersonPerson record
# party_1 = contributor; party_2 = recipient, positive AMT

# TODO: Insert org to people fund transfers
# From Contributor type = contrib_corp, _union, _assoc, _gov --> Recipient type = recip_ent_ppl (filter)
# CONTRIBUTOR: Retrieve id from Organization (exists) or create Organization entry (new)
# RECIPIENT: Retrieve id from People (exists) or create People entry w/ "Political Party of Recipient" membership (new)
# Enter FundingPersonOrg record
# org = contributor; people = recipient, negative AMT

# TODO: Insert people to org fund transfers
# From Contributor type = contrib_ppl --> Recipient type = recip_ent_parties (filter)
# CONTRIBUTOR: Retrieve id from People (exists) or create People entry w/ no memberships (new)
# RECIPIENT: Retrieve id from Organization (exists) or create Organization entry (new)
# Enter FundingPersonOrg record
# people = contributor; org = recipient, positive AMT

# TODO: Insert org to org fund transfers
# From Contributor type = contrib_corp, _union, _assoc, _gov --> Recipient type = recip_ent_parties (filter)
# CONTRIBUTOR: Retrieve id from Organization (exists) or create Organization entry (new)
# RECIPIENT: Retrieve id from Organization (exists) or create Organization entry (new)
# Enter Funding record
# party_1 = contributor; party_2 = recipient, positive AMT
