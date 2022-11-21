from sqlmodel import Session, create_engine, select
from parse_injest.utils import create_match_name
from schema_creation.sqlmodel_build import OrganizationType, Organization, Person, Source, OrganizationMembership

from datetime import date
import glob
import os
import pathlib
import xml.etree.ElementTree as et

data_dir = 'data/members_xml/member_xml'

curr_dir_name = os.path.dirname(__file__)
absolute_ = None
for i in pathlib.Path(curr_dir_name).parents:
    if i.name == 'app':
        absolute_ = i.absolute()
        break

data_dir = os.path.join(absolute_, data_dir)
if not os.path.isdir(data_dir):
    raise RuntimeError("Can't find data directory")


# glob the filenames
file_list = glob.glob(data_dir + "/*.xml")
grab_date = date(2022, 11, 9) #'20221109'

src = Source(date_obtained=grab_date, data_src='OurCommons.ca', misc_data={'url': "ourcommons.ca"})



db_host = "localhost"
db_name = "lq_test"
db_user = "test_user"
db_pw = "changethis"
schema_name = "lf_mockup"

motor = create_engine(f"postgresql+psycopg2://{db_user}:{db_pw}@localhost/{db_name}",  echo=True)
sess = Session(motor)
sql_select = select(Source.id).where(Source.date_obtained == src.date_obtained).where(Source.data_source == src.data_source)
res = sess.exec(sql_select).all()
if len(res) == 0:
    sess.add(src)
    sess.commit()
    res = sess.exec(sql_select).all()
    src_id = res[0]
res_id = res[0]

# get sector id and org type id for Government



member_of_parliament_role_field_list = ['PersonOfficialFirstName',
                                        'PersonOfficialLastName',
                                        'ConstituencyName',
                                        'ConstituencyProvinceTerritoryName',
                                        'CaucusShortName',
                                        'FromDateTime',
                                        'ToDateTime']

for file in file_list[0:1]:
    print(file)

    tree = et.parse(file)
    root = tree.getroot()
    print(root.tag)

    mp_role_dict = {}
    caucus_roles = []
    parliamentary_positions = []
    committee_member_roles = []
    association_and_group_roles = []

    for child in root:
        print(child.tag)

        if child.tag == 'MemberOfParliamentRole':
            for node in child:
                if node.tag in member_of_parliament_role_field_list:
                    mp_role_dict[node.tag] = node.text

        if child.tag == 'CaucusMemberRoles':
            pass

        if child.tag == 'ParliamentaryPositionRoles':
            pass

        if child.tag == 'CommitteeMemberRoles':
            pass

        if child.tag == 'ParliamentaryAssociationsandInterparliamentaryGroups':
            pass

    print(mp_role_dict)


    print("stop")