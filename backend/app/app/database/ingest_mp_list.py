import glob
import xml.etree.ElementTree as et
from DirectoryHandler import DirectoryHandler
import common_func as cf


def insert_mp_people_orgs_memberships(debug_status):
    # Preamble, folder locations
    dh_member_xml = DirectoryHandler("members_xml member_xml")

    # glob the filenames
    file_list = glob.glob(dh_member_xml.path_of_interest + "/*.xml")

    sess = cf.create_session(debug=debug_status)

    # Grab sources (XML Ourcommons)
    dh_member_xml.load_meta_file()
    source_objs = cf.add_sources(sess, [{"data_source": dh_member_xml.source_name,
                                         "date_obtained": dh_member_xml.source_age,
                                         "misc_data": dh_member_xml.source_misc}])

    src_id = source_objs[0].id
    src_date_obtained = dh_member_xml.source_age  # str in isoformat

    member_of_parliament_role_field_list = [
        "PersonOfficialFirstName",
        "PersonOfficialLastName",
        "ConstituencyName",
        "ConstituencyProvinceTerritoryName",
        "CaucusShortName",
        "FromDateTime",
        "ToDateTime",
    ]

    caucus_role_field_list = ["CaucusShortName", "FromDateTime", "ToDateTime"]
    parliamentary_position_field_list = ["Title", "FromDateTime", "ToDateTime"]
    committee_member_field_list = [
        "AffiliationRoleName",
        "CommitteeName",
        "FromDateTime",
        "ToDateTime",
    ]
    association_and_groups_field_list = [
        "AssociationMemberRoleType",
        "Title",
        "Organization",
    ]

    for file in file_list:
        # print(file)

        tree = et.parse(file)
        root = tree.getroot()
        # print(root.tag)

        mp_role_dict = {}
        caucus_roles = []
        parliamentary_positions = []
        committee_member_roles = []
        association_and_group_roles = []

        for child in root:
            # print(child.tag)

            if child.tag == "MemberOfParliamentRole":
                for node in child:
                    if node.tag in member_of_parliament_role_field_list:
                        mp_role_dict[node.tag] = node.text

            elif child.tag == "CaucusMemberRoles":
                for node in child:
                    if node.tag == "CaucusMemberRole":
                        loc_caucus_member_role = {}
                        for n in node:
                            if n.tag in caucus_role_field_list:
                                loc_caucus_member_role[n.tag] = n.text

                        caucus_roles.append(loc_caucus_member_role)

                pass

            elif child.tag == "ParliamentaryPositionRoles":
                for node in child:
                    if node.tag == "ParliamentaryPositionRole":
                        loc_parliamentary_position_role = {}
                        for n in node:
                            if n.tag in parliamentary_position_field_list:
                                loc_parliamentary_position_role[n.tag] = n.text
                        parliamentary_positions.append(loc_parliamentary_position_role)

            elif child.tag == "CommitteeMemberRoles":
                for node in child:
                    if node.tag == "CommitteeMemberRole":
                        loc_committee_member_role = {}
                        for n in node:
                            if n.tag in committee_member_field_list:
                                loc_committee_member_role[n.tag] = n.text
                        committee_member_roles.append(loc_committee_member_role)

            elif child.tag == "ParliamentaryAssociationsandInterparliamentaryGroupRoles":
                for node in child:
                    if (
                        node.tag
                        == "ParliamentaryAssociationsandInterparliamentaryGroupRole"
                    ):
                        loc_association = {}
                        for n in node:
                            if n.tag in association_and_groups_field_list:
                                loc_association[n.tag] = n.text
                        association_and_group_roles.append(loc_association)

        # print(mp_role_dict)

        mp_name = " ".join(
            [
                mp_role_dict["PersonOfficialFirstName"],
                mp_role_dict["PersonOfficialLastName"],
            ]
        )

        federal_riding_name = mp_role_dict["ConstituencyName"] + " - Federal Riding"

        start_date = mp_role_dict["FromDateTime"]  # str in isoformat
        if mp_role_dict["ToDateTime"] is not None:
            end_date = mp_role_dict["ToDateTime"]  # str in isoformat
        else:
            end_date = src_date_obtained

        person_id = cf.add_people(sess, [{"name": mp_name,
                                          "ppl_source_id": src_id}])[0].id

        riding_id = cf.add_organizations(sess, [{"name": federal_riding_name,
                                                 "org_type_str": "government",
                                                 "org_parent_str": "Federal Government of Canada",
                                                 "org_sector_str": "government",
                                                 "org_source_id": src_id,
                                                 }])[0].id

        rid_mem = cf.add_memberships(sess, [{"person_id": person_id,
                                             "org_id": riding_id,
                                             "start_date": start_date,
                                             "end_date": end_date,
                                             "source_id": src_id}])

        # caucus membership
        for c in caucus_roles:
            loc_caucus = " ".join([c['CaucusShortName'].strip(), '- Caucus'])

            cauc_id = cf.add_organizations(sess, [{"name": loc_caucus,
                                                   "org_type_str": "Political Party",
                                                   "org_sector_str": "government",
                                                   "org_source_id": src_id,
                                                   }])[0].id

            sd = c["FromDateTime"]  # str in isoformat
            if c["ToDateTime"] is not None:
                ed = c["ToDateTime"]  # str in isoformat
            else:
                ed = src_date_obtained

            cauc_mem = cf.add_memberships(sess, [{
                "person_id": person_id,
                "org_id": cauc_id,
                "start_date": sd,
                "end_date": ed,
                "source_id": src_id
            }])[0]

        # parliamentary positions
        for p in parliamentary_positions:
            try:
                loc_title = p['Title']

                multi_position = []
                if 'minister of' in loc_title.lower():
                    # if associate is present in the string, wipe it out
                    loc_title = loc_title.replace("Associate", "")
                    # if parliamentary secretary is in a ministry entry, wipe it out
                    loc_title = loc_title.replace("Parliamentary Secretary to the ", '')

                    # how many times is 'minister of' present?
                    if loc_title.lower().count('minister of') > 1:
                        pop_words = ['and', 'the', 'to']
                        cut_string = loc_title

                        ind_1 = cut_string.lower().find('minister', 0)
                        while ind_1 >= 0:
                            ind_2 = cut_string.lower().find('minister', ind_1 + 1)
                            if ind_2 < 0:
                                substring = cut_string[ind_1:].strip()
                                cut_string = ''
                            else:
                                substring = cut_string[ind_1:ind_2].strip()
                                cut_string = cut_string[ind_2:].strip()
                            substring_split = substring.split(' ')
                            substring_split.reverse()
                            start_ind = 0
                            for i in range(0, len(substring_split)):
                                if substring_split[i].lower() in pop_words:
                                    start_ind += 1
                                else:
                                    break
                            substring_split = substring_split[start_ind:]
                            substring_split.reverse()
                            multi_position.append(" ".join(substring_split))
                            ind_1 = cut_string.lower().find('minister', 0)
                    else:
                        multi_position.append(loc_title)

                for loc_title in multi_position:
                    loc_title = loc_title.replace('Minister of', 'Ministry of')

                    loc_title = loc_title.strip()

                    pp_id = cf.add_organizations(sess, [{
                        "name": loc_title,
                        "org_type_str": "Government",
                        "org_sector_str": "Government",
                        "org_parent_str": "Federal Government of Canada",
                        "org_source_id": src_id,
                    }])[0].id

                    sd = p["FromDateTime"]  # str in isoformat
                    if p["ToDateTime"] is not None:
                        ed = p["ToDateTime"]  # str in isoformat
                    else:
                        ed = src_date_obtained

                    pp_mem = cf.add_memberships(sess, [{
                        "person_id": person_id,
                        "org_id": pp_id,
                        "start_date": sd,
                        "end_date": ed,
                        "source_id": src_id
                    }])[0]

            except Exception as e:
                print(e)
                pass

        # committe memberships
        for c in committee_member_roles:
            loc_name = " ".join([c["CommitteeName"], "- Committee"])

            committee_id = cf.add_organizations(sess, [{
                        "name": loc_name,
                        "org_type_str": "Government",
                        "org_sector_str": "Government",
                        "org_parent_str": "Federal Government of Canada",
                        "org_source_id": src_id,
                    }])[0].id

            sd = c["FromDateTime"]  # str in isoformat
            if c["ToDateTime"] is not None:
                ed = c["ToDateTime"]  # str in isoformat
            else:
                ed = src_date_obtained

            committee_membership = cf.add_memberships(sess, [{
                "person_id": person_id,
                "org_id": committee_id,
                "start_date": sd,
                "end_date": ed,
                "source_id": src_id
            }])[0]

        # associations
        for a in association_and_group_roles:
            association_id = cf.add_organizations(sess, [{
                "name": a["Organization"],
                "org_type_str": "Government",
                "org_sector_str": "Government",
                "org_parent_str": "Federal Government of Canada",
                "org_source_id": src_id,
            }])[0].id

            assoc_membership = cf.add_memberships(sess, [{"person_id": person_id,
                                                          "org_id": association_id,
                                                          "start_date": src_date_obtained,
                                                          "end_date": src_date_obtained,
                                                          "source_id": src_id}])

        sess.close()
