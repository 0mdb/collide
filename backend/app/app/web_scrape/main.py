from scrape_corpcan_corp_numbers import scrape_corp_numbers
from scrape_ised_corp_directors import scrape_corp_directors
from scrape_ourcommons_bills_summary import scrape_bill_list
from scrape_ourcommons_bills_detailed import scrape_bill_text
from scrape_ourcommons_votes_summary import scrape_vote_list
from scrape_ourcommons_votes_detailed import scrape_vote_details
from scrape_ourcommons_member import scrape_member_links
from scrape_ourcommons_members_xml_fetch import scrape_member_details
from scrape_ourcommons_cabinet import scrape_cabinet_members


# Pulls corp name from TSX file -> retrieves corp numbers
# May not need to be updated often if TSX file is not changing
print("START")
print("\tstarting corp numbers")
scrape_corp_numbers()
print("\tcompleted corp numbers")

# Uses corp numbers to retrieve current board of directors
print("\tstarting corp directors")
auth_key = None
scrape_corp_directors(auth_key)
print("\tcompleted corp directors")

# Grab list of all bills
print("\tstarting bill list")
scrape_bill_list()
print("\tcompleted bill list")

# Iterates over bill listing to retrieve bill text
print("\tstarting bill text")
scrape_bill_text()
print("\tcompleted bill text")

# Grab list of votes (historically 1 to 7 sessions per parliament)
print("\tstarting vote list")
scrape_vote_list(parl_sessions=["38-1",
                                "39-1", "39-2",
                                "40-1", "40-2", "40-3",
                                "41-1", "41-2",
                                "42-1",
                                "43-1", "43-2",
                                "44-1", "44-2", "44-3"])
print("\tcompleted vote list")

# Iterates over vote listing to retrieve individual voting records
print("\tstarting vote details")
scrape_vote_details()
print("\tcompleted vote details")

# Grab links for each MP in every parliament in range
print("\tstarting member links")
scrape_member_links(parliament_start=36, parliament_end=44)
print("\tcompleted member links")

# Iterates over member links to retrieve member details
print("\tstarting member xml")
scrape_member_details()
print("\tcompleted member xml")

# Grab members of cabinet
# Implicitly assumes ministry=29 (Trudeau)
print("\tstarting cabinet info")
scrape_cabinet_members(precedence_start=77, precedence_end=96)
print("\tcompleted cabinet info")
