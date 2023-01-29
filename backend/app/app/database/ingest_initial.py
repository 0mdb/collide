from datetime import date
import common_func as cf


def insert_entries_for_fresh_db(debug_status):
    # TODO: Test on fresh db 0/1
    # TODO: Test on populated db 1/1

    """
    Run after tables have been created but no entries exist.
    Includes Source, OrganizationType, SectorIndustry, Organization, LegStage entries.

    Returns
    -------

    """

    session = cf.create_session(debug=debug_status)

    # Add initial Source entry
    src_objs = cf.add_sources(session, [{"data_source": "initial inserts",
                                        "date_obtained": date.today()}])
    src_id = src_objs[0].id

    # Add OrganizationType entries
    org_type_list = [
        {"name": "Corporation"},
        {"name": "Government"},
        {"name": "Charity"},
        {"name": "Professional Association"},
        {"name": "Political Party"},
        {"name": "Unclassified"},
        {"name": "Trade Union"}
    ]

    type_objs = cf.add_organization_types(session, org_type_list)

    # Add SectorIndustry for government
    sector_list = [{"sector_name": "Government"}]

    sector_objs = cf.add_sectors(session, sector_list)

    # Add Organization for federal government
    org_list = [{"name": "Federal Government of Canada",
                 "org_type_str": "Government",
                 "org_sector_str": "Government",
                 "org_source_id": src_id,
                 "misc": {}}]

    org_objs = cf.add_organizations(session, org_list)

    # Add LegStage for parliamentary process
    leg_stages = [
        "House Reading First",
        "House Reading Second",
        "House Reading Third",
        "Senate Reading First",
        "Senate Reading Second",
        "Senate Reading Third",
        "Royal Assent"
    ]

    for each_stage in leg_stages:
        stage_obj = cf.add_legstages(session, [{
            "display_name": each_stage
        }])

    session.close()
    print("END")

