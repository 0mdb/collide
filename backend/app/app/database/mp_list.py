from sqlmodel import Session, create_engine, select
from parse_injest.utils import create_match_name
from schema_creation.sqlmodel_build import (
    OrganizationType,
    Organization,
    Person,
    Source,
    OrganizationMembership,
    SectorIndustry,
)

from datetime import date, datetime
import glob
import os
import pathlib
import xml.etree.ElementTree as et

data_dir = "data/members_xml/member_xml"

curr_dir_name = os.path.dirname(__file__)
absolute_ = None
for i in pathlib.Path(curr_dir_name).parents:
    if i.name == "app":
        absolute_ = i.absolute()
        break

data_dir = os.path.join(absolute_, data_dir)
if not os.path.isdir(data_dir):
    raise RuntimeError("Can't find data directory")


# glob the filenames
file_list = glob.glob(data_dir + "/*.xml")

# TODO: fix the source that is grabbed
grab_date = date(2022, 11, 13)  #'20221109'
src = Source(
    date_obtained=grab_date,
    data_source="House of Commons Canada",
    # misc_data={"url": "ourcommons.ca"},
)


db_host = "localhost"
db_name = "lq_test"
db_user = "test_user"
db_pw = "changethis"
schema_name = "lf_mockup"

motor = create_engine(
    f"postgresql+psycopg2://{db_user}:{db_pw}@localhost/{db_name}", echo=False
)
sess = Session(motor)
sql_select = (
    select(Source.id)
    .where(Source.date_obtained == src.date_obtained)
    .where(Source.data_source == src.data_source)
)
res = sess.exec(sql_select).first()
if res is None:
    sess.add(src)
    sess.commit()
    src_id = src.id
else:
    src_id = res

# get sector id and org type id for Government
sql_select = select(OrganizationType.id).where(
    OrganizationType.match_name == create_match_name("Government")
)
res = sess.exec(sql_select).all()
gov_org_type_id = res[0]

sql_select = select(SectorIndustry.id).where(
    SectorIndustry.sector_match_name == create_match_name("Government")
)
res = sess.exec(sql_select).all()
gov_sect_id = res[0]

# get org type for political party
sql_select = select(OrganizationType.id).where(
    OrganizationType.match_name == create_match_name("Political Party")
)
res = sess.exec(sql_select).all()
pol_part_id = res[0]

# get org id for the federal government
sql_select = select(Organization.id).where(
    Organization.match_name == create_match_name("Federal Government of Canada")
)
res = sess.exec(sql_select).all()
fed_gov_id = res[0]

sess.close()

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

    start_date = datetime.fromisoformat(mp_role_dict["FromDateTime"]).date()
    if mp_role_dict["ToDateTime"] is not None:
        end_date = datetime.fromisoformat(mp_role_dict["ToDateTime"]).date()
    else:
        end_date = None

    sess = Session(motor)

    sql_query = select(Person.id).where(Person.match_name == create_match_name(mp_name))
    res = sess.exec(sql_query).first()
    if res is None:
        per = Person(
            display_name=mp_name, match_name=create_match_name(mp_name), source=src_id
        )
        sess.add(per)
        sess.commit()
        person_id = per.id
    else:
        person_id = res

    sql_query = select(Organization.id).where(
        Organization.match_name == create_match_name(federal_riding_name)
    )
    res = sess.exec(sql_query).first()
    if res is None:
        rid = Organization(
            display_name=federal_riding_name,
            match_name=create_match_name(federal_riding_name),
            organization_type=gov_org_type_id,
            sector=gov_sect_id,
            parent_organization=fed_gov_id,
            source=src_id,
        )
        sess.add(rid)
        sess.commit()
        riding_id = rid.id
    else:
        riding_id = res

    sql_query = (
        select(OrganizationMembership.id)
        .where(OrganizationMembership.person == person_id)
        .where(OrganizationMembership.organization == riding_id)
        .where(OrganizationMembership.start_date == start_date)
    )
    res = sess.exec(sql_query).first()
    if res is None:
        rid_mem = OrganizationMembership(
            start_date=start_date,
            end_date=end_date,
            person=person_id,
            organization=riding_id,
            source=src_id,
        )
        sess.add(rid_mem)
        sess.commit()

    # caucus membership
    for c in caucus_roles:
        sql_query = select(Organization.id).where(
            Organization.match_name == create_match_name(c["CaucusShortName"])
        )
        res = sess.exec(sql_query).first()
        if res is None:
            cauc = Organization(
                display_name=c["CaucusShortName"],
                match_name=create_match_name(c["CaucusShortName"]),
                organization_type=pol_part_id,
                sector=gov_sect_id,
                source=src_id,
            )
            sess.add(cauc)
            sess.commit()
            cauc_id = cauc.id
        else:
            cauc_id = res

        sd = datetime.fromisoformat(c["FromDateTime"]).date()
        if c["ToDateTime"] is not None:
            ed = datetime.fromisoformat(c["ToDateTime"]).date()
        else:
            ed = None

        sql_query = (
            select(OrganizationMembership.id)
            .where(OrganizationMembership.person == person_id)
            .where(OrganizationMembership.organization == cauc_id)
        )
        res = sess.exec(sql_query).first()
        if res is None:
            cauc_mem = OrganizationMembership(
                start_date=sd,
                end_date=ed,
                person=person_id,
                organization=cauc_id,
                source=src_id,
            )
            sess.add(cauc_mem)
            sess.commit()

    # parliamentary positions
    for p in parliamentary_positions:
        try:
            sql_query = select(Organization.id).where(
                Organization.match_name == create_match_name(p["Title"])
            )
            res = sess.exec(sql_query).first()
            if res is None:
                pp = Organization(
                    display_name=p["Title"],
                    match_name=create_match_name(p["Title"]),
                    organization_type=gov_org_type_id,
                    sector=gov_sect_id,
                    parent_organization=fed_gov_id,
                    source=src_id,
                )
                sess.add(pp)
                sess.commit()
                pp_id = pp.id
            else:
                pp_id = res

            sd = datetime.fromisoformat(p["FromDateTime"]).date()
            if p["ToDateTime"] is not None:
                ed = datetime.fromisoformat(p["ToDateTime"]).date()
            else:
                ed = None

            sql_query = (
                select(OrganizationMembership.id)
                .where(OrganizationMembership.person == person_id)
                .where(OrganizationMembership.organization == pp_id)
            )
            res = sess.exec(sql_query)
            if res is None:
                pp_mem = OrganizationMembership(
                    person=person_id,
                    organization=pp_id,
                    start_date=sd,
                    end_date=ed,
                    source=src_id,
                )
                sess.add(pp_mem)
                sess.commit()
        except:
            pass

    # committe memberships
    for c in committee_member_roles:
        sql_query = select(Organization.id).where(
            Organization.match_name == create_match_name(c["CommitteeName"])
        )
        res = sess.exec(sql_query).first()
        if res is None:
            committee = Organization(
                display_name=c["CommitteeName"],
                match_name=create_match_name(c["CommitteeName"]),
                organization_type=gov_org_type_id,
                sector=gov_sect_id,
                parent_organization=fed_gov_id,
                source=src_id,
            )
            sess.add(committee)
            sess.commit()
            committee_id = committee.id
        else:
            committee_id = res

        sd = datetime.fromisoformat(c["FromDateTime"]).date()
        if c["ToDateTime"] is not None:
            ed = datetime.fromisoformat(c["ToDateTime"]).date()
        else:
            ed = None

        sql_query = (
            select(OrganizationMembership.id)
            .where(OrganizationMembership.person == person_id)
            .where(OrganizationMembership.organization == committee_id)
            .where(OrganizationMembership.start_date == sd)
        )
        res = sess.exec(sql_query).first()
        if res is None:
            committee_membership = OrganizationMembership(
                person=person_id,
                organization=committee_id,
                start_date=sd,
                end_date=ed,
                source=src_id,
            )
            sess.add(committee_membership)
            sess.commit()

    # associations
    # TODO fix start and end dates for associations
    for a in association_and_group_roles:
        sql_query = select(Organization.id).where(
            Organization.match_name == create_match_name(a["Organization"])
        )
        res = sess.exec(sql_query).first()
        if res is None:
            association = Organization(
                display_name=a["Organization"],
                match_name=create_match_name(a["Organization"]),
                organization_type=gov_org_type_id,
                sector=gov_sect_id,
                parent_organization=fed_gov_id,
                source=src_id,
            )
            sess.add(association)
            sess.commit()
            association_id = association.id
        else:
            association_id = res

        sql_query = (
            select(OrganizationMembership.id)
            .where(OrganizationMembership.person == person_id)
            .where(OrganizationMembership.organization == association_id)
        )
        res = sess.exec(sql_query).first()
        if res is None:
            assoc_membership = OrganizationMembership(
                person=person_id,
                organization=association_id,
                source=src_id,
                start_date=src.date_obtained,
            )
            sess.add(assoc_membership)
            sess.commit()

    # TODO add in code to update the end dates for cases where end date was not available during one import, but available during a later one

    sess.close()
