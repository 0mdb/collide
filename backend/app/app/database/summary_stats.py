import pandas as pd
from sqlmodel import select
from schema_creation.sqlmodel_build import (
    Source,
    Organization,
    OrganizationType,
    SectorIndustry,
    Person,
    OrganizationMembership,
    FundingPersonPerson,
    FundingPersonOrg,
    Funding,
    Bill,
    Vote,
    VoteIndividual,
    BillDiff,
    LegStage,
    CommsTopic, Communications, CommunicationsOrgOrg, CommunicationsPersonOrg
)
import common_func as cf
from datetime import date


session = cf.create_session(debug=False)

summary_df = pd.DataFrame().from_dict({"date_computed": [date.today().strftime('%Y-%m-%d')]})

# NUMBER OF PEOPLE
stat = select(Person.id)
res = session.exec(stat).all()
summary_df["no_people"] = [len(res)]

# TOTAL ELECTION FUNDS
stat = select(Funding.amount)
funding_amt1 = session.exec(stat).all()

stat = select(FundingPersonPerson.amount)
funding_amt2 = session.exec(stat).all()

stat = select(FundingPersonOrg.amount)
funding_amt3 = session.exec(stat).all()

all_funding = funding_amt1 + funding_amt2 + funding_amt3

total_sum = 0
for each_transfer in all_funding:
    total_sum = total_sum + abs(each_transfer)

summary_df["total_funds"] = [total_sum]

# NUMBER LOBBYING COMMUNICATIONS
stat = select(Communications.id)
res = session.exec(stat).all()
summary_df["no_communications"] = [len(res)]

# NUMBER BILLS
stat = select(Bill.id)
res = session.exec(stat).all()
summary_df["no_bills"] = [len(res)]

# NUMBER YEAS AND NAYS
stat = select(Vote.yeas)
yeas_res = session.exec(stat).all()

total_yeas = 0
for each_yea in yeas_res:
    total_yeas = total_yeas + each_yea

summary_df["total_yeas"] = [total_yeas]

stat = select(Vote.nays)
nays_res = session.exec(stat).all()

total_nays = 0
for each_nay in nays_res:
    total_nays = total_nays + each_nay

summary_df["total_nays"] = [total_nays]

# NUMBER OF RECORDS (ALL TABLES)
lst_entries = []
lst_entries.append(len(session.exec(select(Bill.id)).all()))
lst_entries.append(len(session.exec(select(BillDiff.id)).all()))
lst_entries.append(len(session.exec(select(CommsTopic.id)).all()))
lst_entries.append(len(session.exec(select(Communications.id)).all()))
lst_entries.append(len(session.exec(select(CommunicationsOrgOrg.id)).all()))
lst_entries.append(len(session.exec(select(CommunicationsPersonOrg.id)).all()))
lst_entries.append(len(session.exec(select(Funding.id)).all()))
lst_entries.append(len(session.exec(select(FundingPersonOrg.id)).all()))
lst_entries.append(len(session.exec(select(FundingPersonPerson.id)).all()))
lst_entries.append(len(session.exec(select(LegStage.id)).all()))
lst_entries.append(len(session.exec(select(Organization.id)).all()))
lst_entries.append(len(session.exec(select(OrganizationMembership.id)).all()))
lst_entries.append(len(session.exec(select(OrganizationType.id)).all()))
lst_entries.append(len(session.exec(select(Person.id)).all()))
lst_entries.append(len(session.exec(select(SectorIndustry.id)).all()))
lst_entries.append(len(session.exec(select(Source.id)).all()))
lst_entries.append(len(session.exec(select(Vote.id)).all()))
lst_entries.append(len(session.exec(select(VoteIndividual.id)).all()))

total_count = 0
for each_count in lst_entries:
    total_count = total_count + each_count

summary_df["total_db_ids"] = [total_count]

session.close()

summary_df.to_csv("summary_stats.csv")


# TODO: maybe add oldest entry in db?