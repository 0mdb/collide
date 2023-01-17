import pathlib

import common_func as cf
from schema_creation.sqlmodel_build import (
    Organization, OrganizationType, Person, OrganizationMembership,
    FundingPersonPerson, FundingPersonOrg, Funding
)
from sqlmodel import select
import os

search_by_individual = True
entry_threshold = 1
surname_search_lst = []

# TODO: REVAMP AS F(X) FOR INDIVIDUAL MATCH_NAME LOOKUP (VS SURNAME)
# TODO: RUN/CHECK RESULTS

# Preamble, folder locations
project_name = "app"  # collide\backend\app\app
data_dir = "data"
dest_dir = "_sankey"

# Folder creation, directories
curr_dir_name = os.path.dirname(__file__)

absolute_project_path = None
for i in pathlib.Path(curr_dir_name).parents:
    if i.name == project_name:
        absolute_project_path = i.absolute()
        break

dest_dir = os.path.join(absolute_project_path, data_dir, dest_dir)

session = cf.create_session(debug=False)
stat = select(Person)
all_people = session.exec(stat).all()

if search_by_individual:
    fam_results = {}
    for each_person in all_people:
        fam_results[each_person.match_name] = [each_person.id]
else:
    # Used to look up/gather by surname
    surname_lst = []
    for idx, each_person in enumerate(all_people):
        print(f"all ppl loop: {idx} of {len(all_people)}")
        surname_lst.append(each_person.display_name.split()[-1])

    lower_surname_lst = [x.lower() for x in surname_lst]

    # start = time.time()
    fam_results = {}
    for jdx, each_unique_surname in enumerate(surname_search_lst):
        print(f"surname loop: {jdx} of {len(surname_search_lst)}")
        fam_results[each_unique_surname] = []
        for each_person in all_people:
            if each_person.display_name.split()[-1].lower() == each_unique_surname:
                fam_results[each_unique_surname].append(each_person.id)

# end = time.time()
# print(f"timing: {end-start} sec")

fam_results_above_threshold = {}
final_form_json_dict = {}
final_form_json = {"nodes": [],
                   "links": []}
for each_family in fam_results:
    if len(fam_results[each_family]) >= entry_threshold:
        fam_results_above_threshold[each_family] = fam_results[each_family]

# Political parties
stat = select(OrganizationType).where(
    OrganizationType.match_name == "politicalparty"
)
type_party_id = session.exec(stat).all()

stat = select(Organization).where(
    Organization.organization_type == type_party_id[0].id
)
party_orgs = session.exec(stat).all()
party_org_ids = []
party_org_id_display_map = {}
for each_party in party_orgs:
    party_org_ids.append(each_party.id)
    party_org_id_display_map[each_party.id] = each_party.display_name

# Grab person -> person
family_to_people_vals = {}
family_to_people_orgs_vals = {}
for idx, each_family in enumerate(fam_results_above_threshold.keys()):
    print(f"Person2Person loop: {idx} of {len(fam_results_above_threshold.keys())}")
    family_to_people_vals[each_family] = 0
    family_to_people_orgs_vals[each_family] = {}

    for each_party in party_org_ids:
        family_to_people_orgs_vals[each_family][party_org_id_display_map.get(each_party)] = 0

    for each_person_id in fam_results_above_threshold[each_family]:
        stat = select(FundingPersonPerson).where(
            FundingPersonPerson.party_1 == each_person_id
        )
        funds_from_person = session.exec(stat).all()

        for each_tsn in funds_from_person:
            family_to_people_vals[each_family] = family_to_people_vals[each_family] + each_tsn.amount

            recip_id = each_tsn.party_2
            stat = select(OrganizationMembership).where(
                OrganizationMembership.person == recip_id
            ).where(
                OrganizationMembership.start_date <= each_tsn.start_date
            ).where(
                OrganizationMembership.end_date >= each_tsn.start_date
            ).filter(OrganizationMembership.organization.in_(party_org_ids))

            membership_when_funding_received = session.exec(stat).all()

            if len(membership_when_funding_received) > 1:
                print("CONFLICT - more than one membership to party at time of funding")
                print(f"\t\tRecipient id {recip_id}")
                print(f"\t\tTrx date {each_tsn.start_date}")

            id_key_party = membership_when_funding_received[0].organization
            display_key_party = party_org_id_display_map.get(id_key_party)
            family_to_people_orgs_vals[each_family][display_key_party] = family_to_people_orgs_vals[each_family][
                                                                             display_key_party] + each_tsn.amount

for each_family in family_to_people_vals.keys():
    final_form_json_dict[each_family] = final_form_json
    final_form_json_dict[each_family]["links"].append({"source": each_family,
                                                       "target": f"election candidates",
                                                       "value": family_to_people_vals[each_family]})

for each_family in family_to_people_orgs_vals.keys():
    for each_party in family_to_people_orgs_vals[each_family].keys():
        final_form_json_dict[each_family]["links"].append({"source": f"election candidates",
                                                           "target": each_party,
                                                           "value": family_to_people_orgs_vals[each_family][
                                                               each_party]})

# People to org to party funding
# Grab person -> org
family_to_riding_vals = {}
family_to_riding_party_vals = {}
family_to_party_vals = {}
for idx, each_family in enumerate(fam_results_above_threshold.keys()):
    print(f"Person2Org loop: {idx} of {len(fam_results_above_threshold.keys())}")
    family_to_riding_vals[each_family] = 0
    family_to_riding_party_vals[each_family] = {}
    family_to_party_vals[each_family] = {}

    for each_party in party_org_ids:
        family_to_riding_party_vals[each_family][party_org_id_display_map.get(each_party)] = 0
        family_to_party_vals[each_family][party_org_id_display_map.get(each_party)] = 0

    for each_person_id in fam_results_above_threshold[each_family]:
        stat = select(FundingPersonOrg).where(
            FundingPersonOrg.person == each_person_id
        ).where(
            FundingPersonOrg.amount > 0
        )
        funds_from_person = session.exec(stat).all()

        for each_tsn in funds_from_person:
            recip_id = each_tsn.organization

            # each_tsn directly to party
            if recip_id in party_org_ids:
                recip_party_id = recip_id
                family_to_party_vals[each_family][party_org_id_display_map.get(recip_id)] = \
                family_to_party_vals[each_family][party_org_id_display_map.get(recip_id)] + each_tsn.amount
            # each_tsn to riding org then to party
            else:
                family_to_riding_vals[each_family] = family_to_riding_vals[each_family] + each_tsn.amount
                stat = select(Organization).where(
                    Organization.id == recip_id
                )
                ret = session.exec(stat).all()
                recip_party_id = ret[0].parent_organization

                display_key_party = party_org_id_display_map.get(recip_party_id)
                family_to_riding_party_vals[each_family][display_key_party] = family_to_riding_party_vals[each_family][
                                                                                  display_key_party] + each_tsn.amount

for each_family in family_to_riding_vals.keys():
    final_form_json_dict[each_family]["links"].append({"source": each_family,
                                                       "target": f"riding associations",
                                                       "value": family_to_riding_vals[each_family]})

for each_family in family_to_riding_party_vals.keys():
    for each_party in family_to_riding_party_vals[each_family].keys():
        final_form_json_dict[each_family]["links"].append({"source": f"riding associations",
                                                           "target": each_party,
                                                           "value": family_to_riding_party_vals[each_family][
                                                               each_party]})

for each_family in family_to_party_vals.keys():
    for each_party in family_to_party_vals[each_family].keys():
        final_form_json_dict[each_family]["links"].append({"source": each_family,
                                                           "target": each_party,
                                                           "value": family_to_party_vals[each_family][each_party]})

# Remove links with value = 0, trim nodes
for each_family in family_to_party_vals.keys():
    trimmed_link_list = [x for x in final_form_json_dict[each_family]["links"] if x.get("value") > 0]
    final_form_json_dict[each_family]["links"] = trimmed_link_list
    source_nodes = [{"name": x.get("source")} for x in final_form_json_dict[each_family]["links"]]
    target_nodes = [{"name": x.get("target")} for x in final_form_json_dict[each_family]["links"]]
    nodes_list = source_nodes + target_nodes
    nodes_list = [dict(t) for t in {tuple(d.items()) for d in nodes_list}]
    final_form_json_dict[each_family]["nodes"] = nodes_list

import json

for every_json_match_name in final_form_json_dict.keys():
    with open(os.path.join(dest_dir, f"{every_json_match_name}_sankey.json"), 'w') as f:
        json.dump(final_form_json_dict[every_json_match_name], f)

# TODO: Mine people -> org -> party table/route??

print("END")
session.close()

#
#
# final_form_json = {
#     "nodes": [
#         {"name": "string value"},
#         {"name": "string value"}
#     ],
#     "links": [
#         {"source": "from_node", "target": "to_node", "value": float},
#         {"source": "from_node", "target": "to_node", "value": float}
#     ]
# }
