import pathlib

import common_func as cf
from schema_creation.sqlmodel_build import (
    Organization, OrganizationType, Person, OrganizationMembership,
    FundingPersonPerson, FundingPersonOrg, Funding
)
from sqlmodel import select
import os
import json


def create_sankey_from_individual(search_match_name):
    """
    final_form_json = {
        "nodes": [
            {"name": "string value"},
            {"name": "string value"}
        ],
        "links": [
            {"source": "from_node", "target": "to_node", "value": float},
            {"source": "from_node", "target": "to_node", "value": float}
        ]
    }

    Parameters
    ----------
    search_match_name

    Returns
    -------

    """

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

    final_form_json = {"nodes": [],
                       "links": []}

    session = cf.create_session(debug=False)
    stat = select(Person).where(
        Person.match_name == search_match_name
    )
    person_of_interest = session.exec(stat).first()

    # Political parties org type
    stat = select(OrganizationType.id).where(
        OrganizationType.match_name == "politicalparty"
    )
    type_party_id = session.exec(stat).first()

    # Political parties orgs
    stat = select(Organization).where(
        Organization.organization_type == type_party_id
    )
    party_orgs = session.exec(stat).all()

    party_org_ids = []
    party_org_id_display_map = {}

    poi_to_people_vals = 0
    poi_to_people_orgs_vals = {}

    for each_party in party_orgs:
        party_org_ids.append(each_party.id)
        party_org_id_display_map[each_party.id] = each_party.display_name
        poi_to_people_orgs_vals[each_party.display_name] = 0

    # Grab person_of_interest -> person
    stat = select(FundingPersonPerson).where(
        FundingPersonPerson.party_1 == person_of_interest.id
    )
    funds_from_poi = session.exec(stat).all()

    for each_tsn in funds_from_poi:
        poi_to_people_vals = poi_to_people_vals + each_tsn.amount
        recip_id = each_tsn.party_2

        stat = select(OrganizationMembership).where(
            OrganizationMembership.person == recip_id
        ).where(
            OrganizationMembership.start_date <= each_tsn.start_date
        ).where(
            OrganizationMembership.end_date >= each_tsn.start_date
        ).filter(OrganizationMembership.organization.in_(party_org_ids))

        recip_membership_when_funding_received = session.exec(stat).all()

        if len(recip_membership_when_funding_received) > 1:
            print("CONFLICT - more than one membership to party at time of funding")
            print(f"\t\tRecipient id {recip_id}")
            print(f"\t\tTrx date {each_tsn.start_date}")

        id_recip_party = recip_membership_when_funding_received[0].organization
        display_recip_party = party_org_id_display_map.get(id_recip_party)
        poi_to_people_orgs_vals[display_recip_party] = poi_to_people_orgs_vals[display_recip_party] + each_tsn.amount

    final_form_json_dict = final_form_json
    final_form_json_dict["links"].append({"source": person_of_interest.display_name,
                                          "target": f"election candidates",
                                          "value": poi_to_people_vals})

    for each_party in poi_to_people_orgs_vals.keys():
        final_form_json_dict["links"].append({"source": f"election candidates",
                                              "target": each_party,
                                              "value": poi_to_people_orgs_vals[each_party]})

    # People to org to party funding
    # Grab person -> org
    poi_to_riding_vals = 0
    poi_to_riding_party_vals = {}
    poi_to_party_vals = {}

    for each_party in party_org_ids:
        poi_to_riding_party_vals[party_org_id_display_map.get(each_party)] = 0
        poi_to_party_vals[party_org_id_display_map.get(each_party)] = 0

    stat = select(FundingPersonOrg).where(
        FundingPersonOrg.person == person_of_interest.id
    ).where(
        FundingPersonOrg.amount > 0
    )
    funds_from_person = session.exec(stat).all()

    for each_tsn in funds_from_person:
        recip_id = each_tsn.organization

        # each_tsn directly to party
        if recip_id in party_org_ids:
            recip_party_id = recip_id
            poi_to_party_vals[party_org_id_display_map.get(recip_id)] = poi_to_party_vals[party_org_id_display_map.get(recip_id)] + each_tsn.amount
        # each_tsn to riding org then to party
        else:
            poi_to_riding_vals = poi_to_riding_vals + each_tsn.amount
            stat = select(Organization).where(
                Organization.id == recip_id
            )
            ret = session.exec(stat).first()
            recip_party_id = ret.parent_organization

            display_key_party = party_org_id_display_map.get(recip_party_id)
            poi_to_riding_party_vals[display_key_party] = poi_to_riding_party_vals[display_key_party] + each_tsn.amount

    final_form_json_dict["links"].append({"source": person_of_interest.display_name,
                                          "target": f"riding associations",
                                          "value": poi_to_riding_vals})

    for each_party in poi_to_riding_party_vals.keys():
        final_form_json_dict["links"].append({"source": f"riding associations",
                                              "target": each_party,
                                              "value": poi_to_riding_party_vals[each_party]})

        final_form_json_dict["links"].append({"source": person_of_interest.display_name,
                                              "target": each_party,
                                              "value": poi_to_party_vals[each_party]})

    # Remove links with value = 0, trim nodes
    trimmed_link_list = [x for x in final_form_json_dict["links"] if x.get("value") > 0]
    final_form_json_dict["links"] = trimmed_link_list
    source_nodes = [{"name": x.get("source")} for x in final_form_json_dict["links"]]
    target_nodes = [{"name": x.get("target")} for x in final_form_json_dict["links"]]
    nodes_list = source_nodes + target_nodes
    nodes_list = [dict(t) for t in {tuple(d.items()) for d in nodes_list}]
    final_form_json_dict["nodes"] = nodes_list

    with open(os.path.join(dest_dir, f"{person_of_interest.match_name}_sankey.json"), 'w') as f:
        json.dump(final_form_json_dict, f)

    session.close()
    print("END")


create_sankey_from_individual("michaelwilson")
