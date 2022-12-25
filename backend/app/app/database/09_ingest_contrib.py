import datetime
import glob
import os
import pathlib
import pandas as pd
import common_func as cf


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

    def __init__(self, file_paths):
        for each_file in file_paths:
            if "meta" in str(each_file):
                self.meta_path = each_file
            else:
                self.data_path = each_file

        self.df = None
        self.transactions = None
        self.date_scraped = None
        self.source_name = None
        self.source_url = None

        self.recip_ent_ppl = ["candidates",
                              "leadership contestants",
                              "nomination contestants"]

        self.recip_ent_parties = ["registered parties",
                                  "registered associations"]

        self.contrib_ppl = ["individuals"]
        self.contrib_corp = ["corporations"]
        self.contrib_bus = ["businesses"]
        self.contrib_union = ["trade"]
        self.contrib_assoc = ["associations"]
        self.contrib_gov = ["governments"]

    def load_csv(self):
        self.df = pd.read_csv(self.data_path, nrows=100)

        # Person to Org donation example (not in first 100 rows)
        # self.df = pd.read_csv(self.data_path, nrows=358695)
        # self.df = self.df.iloc[358595:]

    def load_meta_txt(self):
        temp_df = pd.read_csv(self.meta_path)
        self.date_scraped = temp_df["date_scraped"].to_list()[0]
        self.source_name = temp_df["source_name"].to_list()[0]
        self.source_url = temp_df["source_url"].to_list()[0]

    def build_transactions(self):
        pe = self.df["Political Entity"].to_list()
        rl = self.df["Recipient last name"].to_list()
        rf = self.df["Recipient first name"].to_list()
        p = self.df["Political Party of Recipient"].to_list()
        d = self.df["Fiscal/Election date"].to_list()

        ct = self.df["Contributor type"].to_list()
        col = self.df["Contributor last name"].to_list()
        cof = self.df["Contributor first name"].to_list()
        amt = self.df["Monetary amount"].to_list()
        other_amt = self.df["Non-Monetary amount"].to_list()

        tsn = []
        for idx, each_pe in enumerate(pe):
            tsn.append(Transaction(str(pe[idx]),
                                   str(rf[idx]),
                                   str(rl[idx]),
                                   str(p[idx]),
                                   str(d[idx]),
                                   str(ct[idx]),
                                   str(cof[idx]),
                                   str(col[idx]),
                                   int(abs(float(amt[idx]))+abs(float(other_amt[idx])))
                                   )
                       )
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

contrib_csv = glob.glob(contrib_dir + "/*.csv")

if len(contrib_csv) > 2:
    raise RuntimeError("More than two csv detected.")

election_csv = ElxCsv(contrib_csv)
election_csv.load_csv()
election_csv.load_meta_txt()
election_csv.build_transactions()

threshold_amt = 500.0
tsn_above_threshold = [x for x in election_csv.transactions if x.amt >= threshold_amt]

session = cf.create_session()

src_objs = cf.add_sources(session,
                          [{
                              "data_source": election_csv.source_name,
                              "date_obtained": datetime.datetime.fromisoformat(election_csv.date_scraped).date(),
                              "misc_data": {"filenames": [os.path.basename(election_csv.data_path)],
                                            "url": election_csv.source_url}
                          }])

# Insert people to people fund transfers
# From Contributor type con_type = contrib_ppl --> Recipient type pol_ent = recip_ent_ppl (filter)
tsn_p2p = [x for x in tsn_above_threshold if (x.con_type.lower() in election_csv.contrib_ppl) and (x.pol_ent.lower() in election_csv.recip_ent_ppl)]

for each_tsn in tsn_p2p:
    # CONTRIBUTOR: Retrieve id from People (exists) or create People entry w/ no memberships (new)
    contrib_obj = cf.add_people(session, [{
            "name": f"{each_tsn.con_f} {each_tsn.con_l}",
            "ppl_source_id": src_objs[0].id
        }])

    # RECIPIENT: Retrieve id from People (exists) or
    # create People entry w/ "Political Party of Recipient" membership (new)
    # Add recipient (person)
    recip_obj = cf.add_people(session, [{
        "name": f"{each_tsn.recip_f} {each_tsn.recip_l}",
        "ppl_source_id": src_objs[0].id
    }])

    # Add organization that recipient is a member of (political party)
    recip_party_name = each_tsn.recip_party
    if each_tsn.recip_party == "No Affiliation":
        recip_party_name = "Independent"

    recip_org_obj = cf.add_organizations(session, [{
        "name": recip_party_name,
        "org_type_str": "Political Party",
        "org_sector_str": "Government",
        "org_source_id": src_objs[0].id,
        "misc": {}

    }])

    # Add membership of recipient to organization
    recip_mem_obj = cf.add_memberships(session, [{
        "person_id": recip_obj[0].id,
        "org_id": recip_org_obj[0].id,
        "start_date": each_tsn.fiscal_date,
        "end_date": each_tsn.fiscal_date,
        "source_id": src_objs[0].id,
    }])

    # party_1 = contributor; party_2 = recipient, positive AMT
    funds_obj = cf.add_funding_p2p(session, [{
        "party_1": contrib_obj[0].id,
        "party_2": recip_obj[0].id,
        "amount": each_tsn.amt,
        "start_date": each_tsn.fiscal_date,
        "end_date": each_tsn.fiscal_date,
        "source_id": src_objs[0].id
    }])

# Insert org to people fund transfers
# From Contributor type = contrib_corp, _union, _assoc, _gov --> Recipient type = recip_ent_ppl (filter)
contrib_org_list = election_csv.contrib_corp + election_csv.contrib_union + election_csv.contrib_assoc + election_csv.contrib_gov + election_csv.contrib_bus
tsn_o2p = [x for x in tsn_above_threshold if (x.con_type.lower() in contrib_org_list) and (x.pol_ent.lower() in election_csv.recip_ent_ppl)]

for each_tsn in tsn_o2p:
    # CONTRIBUTOR: Retrieve id from Organization (exists) or create Organization entry (new)
    con_org_type = cf.match_ecanada_contrib_org_type(each_tsn.con_type)

    contrib_org_obj = cf.add_organizations(session, [{
        "name": each_tsn.con_l,  # org name held in last name position
        "org_type_str": con_org_type,
        # "org_sector_str": "",
        "org_source_id": src_objs[0].id,
        "misc": {}
    }])

    # RECIPIENT: Retrieve id from People (exists)
    # or create People entry w/ "Political Party of Recipient" membership (new)
    recip_obj = cf.add_people(session, [{
        "name": f"{each_tsn.recip_f} {each_tsn.recip_l}",
        "ppl_source_id": src_objs[0].id
    }])

    recip_party_name = each_tsn.recip_party
    if each_tsn.recip_party == "No Affiliation":
        recip_party_name = "Independent"

    recip_org_obj = cf.add_organizations(session, [{
        "name": recip_party_name,
        "org_type_str": "Political Party",
        "org_sector_str": "Government",
        "org_source_id": src_objs[0].id,
        "misc": {}
    }])

    recip_mem_obj = cf.add_memberships(session, [{
        "person_id": recip_obj[0].id,
        "org_id": recip_org_obj[0].id,
        "start_date": each_tsn.fiscal_date,
        "end_date": each_tsn.fiscal_date,
        "source_id": src_objs[0].id,
    }])

    # Enter FundingPersonOrg record
    # org = contributor; people = recipient, negative AMT
    funds_obj = cf.add_funding_p2o(session, [{
        "organization": contrib_org_obj[0].id,
        "person": recip_obj[0].id,
        "amount": -1 * each_tsn.amt,
        "start_date": each_tsn.fiscal_date,
        "end_date": each_tsn.fiscal_date,
        "source_id": src_objs[0].id
    }])

# From Contributor type = contrib_ppl --> Recipient type = recip_ent_parties (filter)
tsn_p2o = [x for x in tsn_above_threshold if (x.con_type.lower() in election_csv.contrib_ppl) and (x.pol_ent.lower() in election_csv.recip_ent_parties)]

for each_tsn in tsn_p2o:
    # CONTRIBUTOR: Retrieve id from People (exists) or create People entry w/ no memberships (new)
    contrib_obj = cf.add_people(session, [{
        "name": f"{each_tsn.con_f} {each_tsn.con_l}",
        "ppl_source_id": src_objs[0].id
    }])

    # RECIPIENT: Retrieve id from Organization (exists) or create Organization entry (new)
    # Recipient association/org has parent Political Party (**assuming always)
    recip_parent_org_obj = cf.add_organizations(session, [{
            "name": each_tsn.recip_party,
            "org_type_str": "Political Party",
            # "org_parent_str": "",
            "org_sector_str": "Government",
            "org_source_id": src_objs[0].id,
            "misc": {}

    }])

    recip_org_type = cf.match_ecanada_recip_org_type(each_tsn.pol_ent)

    recip_org_obj = cf.add_organizations(session, [{
        "name": each_tsn.recip_l,  # org name held in last name position
        "org_type_str": recip_org_type,
        "org_parent_str": each_tsn.recip_party,
        # "org_sector_str": "",
        "org_source_id": src_objs[0].id,
        "misc": {}
    }])

    # Enter FundingPersonOrg record
    # people = contributor; org = recipient, positive AMT
    funds_obj = cf.add_funding_p2o(session, [{
        "organization": recip_org_obj[0].id,
        "person": contrib_obj[0].id,
        "amount": each_tsn.amt,
        "start_date": each_tsn.fiscal_date,
        "end_date": each_tsn.fiscal_date,
        "source_id": src_objs[0].id
    }])

print("DONE")

# TODO: Insert org to org fund transfers
# From Contributor type = contrib_corp, _union, _assoc, _gov --> Recipient type = recip_ent_parties (filter)
# CONTRIBUTOR: Retrieve id from Organization (exists) or create Organization entry (new)
# RECIPIENT: Retrieve id from Organization (exists) or create Organization entry (new)
# Enter Funding record
# party_1 = contributor; party_2 = recipient, positive AMT
