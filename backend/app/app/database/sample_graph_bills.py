import common_func as cf
from sqlmodel import Session, create_engine, select, or_
from schema_creation.sqlmodel_build import (
    Bill, Vote, VoteIndividual, Communications, LegStage, Person
)
import json
import datetime

bill_lookup = "40_2_c-50"

session = cf.create_session(debug=False)
stat = select(Bill).where(
    Bill.match_name == bill_lookup
)
res = session.exec(stat).all()

if len(res) != 1:
    raise AssertionError("wrong")
bill = res[0]

########################################

stat = select(LegStage)
all_stages = session.exec(stat).all()
legstage_map = {}
for each_leg_stage in all_stages:
    if each_leg_stage.match_name == "housereadingfirst":
        legstage_map["first-reading-house"] = (each_leg_stage.id, each_leg_stage.display_name)
    if each_leg_stage.match_name == "housereadingsecond":
        legstage_map["second-reading-house"] = (each_leg_stage.id, each_leg_stage.display_name)
        legstage_map["report-house"] = (each_leg_stage.id, each_leg_stage.display_name)
    if each_leg_stage.match_name == "housereadingthird":
        legstage_map["third-reading-house"] = (each_leg_stage.id, each_leg_stage.display_name)
    if each_leg_stage.match_name == "senatereadingfirst":
        legstage_map["first-reading-senate"] = (each_leg_stage.id, each_leg_stage.display_name)
    if each_leg_stage.match_name == "senatereadingsecond":
        legstage_map["second-reading-senate"] = (each_leg_stage.id, each_leg_stage.display_name)
    if each_leg_stage.match_name == "senatereadingthird":
        legstage_map["third-reading-senate"] = (each_leg_stage.id, each_leg_stage.display_name)
    if each_leg_stage.match_name == "royalassent":
        legstage_map["assented-to"] = (each_leg_stage.id, each_leg_stage.display_name)

########################################

nodes_links_dict = {"nodes": [],
                    "links": []}
node_color_bill_line = 'black'
node_color_vote = {"yea": 'green',
                   "nay": 'red',
                   "paired": 'grey'}
node_color_outsider = 'purple'

stage_dates = {}
stage_listing = []
all_stage_listing = []
node_id_lst = []

if bill.is_house_bill:
    if bill.is_read_first_house:
        # add first house reading
        stage_lst = legstage_map["first-reading-house"]
        leg_id = stage_lst[0]
        leg_name = stage_lst[1]
        nodes_links_dict["nodes"].append({
            "id": hash(stage_lst),
            "legstage_id": leg_id,
            "name": leg_name,  # display name
            "nodeColor": node_color_bill_line,
            "nodeVal": 8
        })
        stage_dates[hash(stage_lst)] = bill.first_house_read_date
        stage_listing.append(hash(stage_lst))
        all_stage_listing.append(hash(stage_lst))

    if bill.is_read_second_house:
        # add second house reading
        stage_lst = legstage_map["second-reading-house"]
        leg_id = stage_lst[0]
        leg_name = stage_lst[1]
        nodes_links_dict["nodes"].append({
            "id": hash(stage_lst),
            "legstage_id": leg_id,
            "name": leg_name,  # display name
            "nodeColor": node_color_bill_line,
            "nodeVal": 8
        })
        stage_dates[hash(stage_lst)] = bill.second_house_read_date
        stage_listing.append(hash(stage_lst))
        all_stage_listing.append(hash(stage_lst))

    if bill.is_read_third_house:
        # add third house reading
        stage_lst = legstage_map["third-reading-house"]
        leg_id = stage_lst[0]
        leg_name = stage_lst[1]
        nodes_links_dict["nodes"].append({
            "id": hash(stage_lst),
            "legstage_id": leg_id,
            "name": leg_name,  # display name
            "nodeColor": node_color_bill_line,
            "nodeVal": 8
        })
        stage_dates[hash(stage_lst)] = bill.third_house_read_date
        stage_listing.append(hash(stage_lst))
        all_stage_listing.append(hash(stage_lst))

    if bill.is_read_first_senate:
        # add first senate reading
        stage_lst = legstage_map["first-reading-senate"]
        leg_id = stage_lst[0]
        leg_name = stage_lst[1]
        nodes_links_dict["nodes"].append({
            "id": hash(stage_lst),
            "legstage_id": leg_id,
            "name": leg_name,  # display name
            "nodeColor": node_color_bill_line,
            "nodeVal": 8
        })
        stage_dates[hash(stage_lst)] = bill.first_senate_read_date
        all_stage_listing.append(hash(stage_lst))

    if bill.is_read_second_senate:
        # add second senate reading
        stage_lst = legstage_map["second-reading-senate"]
        leg_id = stage_lst[0]
        leg_name = stage_lst[1]
        nodes_links_dict["nodes"].append({
            "id": hash(stage_lst),
            "legstage_id": leg_id,
            "name": leg_name,  # display name
            "nodeColor": node_color_bill_line,
            "nodeVal": 8
        })
        stage_dates[hash(stage_lst)] = bill.second_senate_read_date
        all_stage_listing.append(hash(stage_lst))

    if bill.is_read_third_senate:
        # add third senate reading
        stage_lst = legstage_map["third-reading-senate"]
        leg_id = stage_lst[0]
        leg_name = stage_lst[1]
        nodes_links_dict["nodes"].append({
            "id": hash(stage_lst),
            "legstage_id": leg_id,
            "name": leg_name,  # display name
            "nodeColor": node_color_bill_line,
            "nodeVal": 8
        })
        stage_dates[hash(stage_lst)] = bill.third_senate_read_date
        all_stage_listing.append(hash(stage_lst))

elif bill.is_senate_bill:
    if bill.is_read_first_senate:
        # add first senate reading
        stage_lst = legstage_map["first-reading-senate"]
        leg_id = stage_lst[0]
        leg_name = stage_lst[1]
        nodes_links_dict["nodes"].append({
            "id": hash(stage_lst),
            "legstage_id": leg_id,
            "name": leg_name,  # display name
            "nodeColor": node_color_bill_line,
            "nodeVal": 8
        })
        stage_dates[hash(stage_lst)] = bill.first_senate_read_date
        all_stage_listing.append(hash(stage_lst))

    if bill.is_read_second_senate:
        # add second senate reading
        stage_lst = legstage_map["second-reading-senate"]
        leg_id = stage_lst[0]
        leg_name = stage_lst[1]
        nodes_links_dict["nodes"].append({
            "id": hash(stage_lst),
            "legstage_id": leg_id,
            "name": leg_name,  # display name
            "nodeColor": node_color_bill_line,
            "nodeVal": 8
        })
        stage_dates[hash(stage_lst)] = bill.second_senate_read_date
        all_stage_listing.append(hash(stage_lst))

    if bill.is_read_third_senate:
        # add third senate reading
        stage_lst = legstage_map["third-reading-senate"]
        leg_id = stage_lst[0]
        leg_name = stage_lst[1]
        nodes_links_dict["nodes"].append({
            "id": hash(stage_lst),
            "legstage_id": leg_id,
            "name": leg_name,  # display name
            "nodeColor": node_color_bill_line,
            "nodeVal": 8
        })
        stage_dates[hash(stage_lst)] = bill.third_senate_read_date
        all_stage_listing.append(hash(stage_lst))

    if bill.is_read_first_house:
        # add first house reading
        stage_lst = legstage_map["first-reading-house"]
        leg_id = stage_lst[0]
        leg_name = stage_lst[1]
        nodes_links_dict["nodes"].append({
            "id": hash(stage_lst),
            "legstage_id": leg_id,
            "name": leg_name,  # display name
            "nodeColor": node_color_bill_line,
            "nodeVal": 8
        })
        stage_dates[hash(stage_lst)] = bill.first_house_read_date
        stage_listing.append(hash(stage_lst))
        all_stage_listing.append(hash(stage_lst))

    if bill.is_read_second_house:
        # add second house reading
        stage_lst = legstage_map["second-reading-house"]
        leg_id = stage_lst[0]
        leg_name = stage_lst[1]
        nodes_links_dict["nodes"].append({
            "id": hash(stage_lst),
            "legstage_id": leg_id,
            "name": leg_name,  # display name
            "nodeColor": node_color_bill_line,
            "nodeVal": 8
        })
        stage_dates[hash(stage_lst)] = bill.second_house_read_date
        stage_listing.append(hash(stage_lst))
        all_stage_listing.append(hash(stage_lst))

    if bill.is_read_third_house:
        # add third house reading
        stage_lst = legstage_map["third-reading-house"]
        leg_id = stage_lst[0]
        leg_name = stage_lst[1]
        nodes_links_dict["nodes"].append({
            "id": hash(stage_lst),
            "legstage_id": leg_id,
            "name": leg_name,  # display name
            "nodeColor": node_color_bill_line,
            "nodeVal": 8
        })
        stage_dates[hash(stage_lst)] = bill.third_house_read_date
        stage_listing.append(hash(stage_lst))
        all_stage_listing.append(hash(stage_lst))

if bill.is_passed_royal_assent:
    # add royal assent
    stage_lst = legstage_map["assented-to"]
    leg_id = stage_lst[0]
    leg_name = stage_lst[1]
    nodes_links_dict["nodes"].append({
        "id": hash(stage_lst),
        "legstage_id": leg_id,
        "name": leg_name,  # display name
        "nodeColor": node_color_bill_line,
        "nodeVal": 8
    })
    stage_dates[hash(stage_lst)] = bill.royal_assent_date
    all_stage_listing.append(hash(stage_lst))

node_id_lst = node_id_lst + all_stage_listing

# Build links between bill stages
for idx, each_stage_hash in enumerate(all_stage_listing[:-1]):
    nodes_links_dict["links"].append({
        "source": all_stage_listing[idx],
        "target": all_stage_listing[idx+1],
        "linkColor": node_color_bill_line,
        "linkDirectionalArrowLength": 6,  # 0 removes
        "linkDirectionalArrowRelPos": 0.5,
        "linkWidth": 4
    })

########################################

# query votes by bill stage
for each_stage_hash in stage_listing:
    # retrieve vote id when bill.id matches, date matches
    stat = select(Vote).where(
        Vote.bill == bill.id
    ).where(
        Vote.date_held == stage_dates[each_stage_hash]
    )
    res = session.exec(stat).all()

    if len(res) == 1:
        # Find VoteIndividual by Vote.id, add nodes, add links
        stat = select(VoteIndividual).where(
            VoteIndividual.vote == res[0].id
        )
        res = session.exec(stat).all()

        for each_individual_vote in res:
            person_id = each_individual_vote.person
            if each_individual_vote.is_yea:
                person_vote = "yea"
            elif each_individual_vote.is_nay:
                person_vote = "nay"
            else:
                person_vote = "paired"

            stat = select(Person).where(
                Person.id == person_id
            )
            res = session.exec(stat).all()

            person_name = res[0].display_name
            person_hash = hash((res[0].match_name, stage_dates[each_stage_hash]))

            # Nodes by person/vote date
            if person_hash not in node_id_lst:
                nodes_links_dict["nodes"].append({
                    "id": person_hash,
                    "legstage_id": -1,
                    "name": person_name,  # display name
                    "nodeColor": node_color_vote[person_vote],
                    "nodeVal": 2
                })
                node_id_lst.append(person_hash)

            # Links person -> vote
            nodes_links_dict["links"].append({
                "source": person_hash,
                "target": each_stage_hash,
                "linkColor": node_color_vote[person_vote],
                "linkDirectionalArrowLength": 0,  # 0 removes
                "linkDirectionalArrowRelPos": 0,
                "linkWidth": 1
            })

            # query comms logs for communications within 30 days of vote date
            stat = select(Communications).where(
                or_(Communications.party_1 == person_id, Communications.party_2 == person_id)
            ).where(
                Communications.com_date <= stage_dates[each_stage_hash]
            ).where(
                Communications.com_date > stage_dates[each_stage_hash] - datetime.timedelta(days=30)
            )
            res = session.exec(stat).all()

            # loop over entries, add nodes, add links
            for each_communication in res:
                if each_communication.party_1 == person_id:
                    other_person_id = each_communication.party_2
                else:
                    other_person_id = each_communication.party_1

                stat_other_party = select(Person).where(
                    Person.id == other_person_id
                )
                res_other_party = session.exec(stat_other_party).all()

                other_person_hash = hash((res_other_party[0].match_name, each_communication.com_date))

                if other_person_hash not in node_id_lst:
                    nodes_links_dict["nodes"].append({
                        "id": other_person_hash,
                        "legstage_id": -1,
                        "name": res_other_party[0].display_name,  # display name
                        "nodeColor": node_color_outsider,
                        "nodeVal": 2
                    })
                    node_id_lst.append(other_person_hash)

                # Links other_person -> voting_person
                nodes_links_dict["links"].append({
                    "source": other_person_hash,
                    "target": person_hash,
                    "linkColor": node_color_outsider,
                    "linkDirectionalArrowLength": 0,  # 0 removes
                    "linkDirectionalArrowRelPos": 0,
                    "linkWidth": 1
                })

print(nodes_links_dict)
with open("testing.json", 'w') as f:
    json.dump(nodes_links_dict, f, indent=4)

print("END")

"""
{"nodes": [
    {
    "id": str,
    "name": str,  # display name
    "nodeColor": 'green'
    }
    ]
"links": [
    {
    "source": str,
    "target": str,
    "linkColor": 'purple',
    "linkDirectionalArrowLength"={3.5}  # 0 removes
    "linkDirectionalArrowRelPos"={1}
    }
    ]
}


"""