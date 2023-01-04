import datetime
import glob
import os
import pathlib
import pandas as pd
import common_func as cf
import xml.etree.ElementTree as et

# Preamble, folder locations
project_name = "app"  # collide\backend\app\app
data_dir = "data"
data_dir_bills_detailed = os.path.join("bills", "detail")

# Folder creation, directories
curr_dir_name = os.path.dirname(__file__)

absolute_project_path = None
for i in pathlib.Path(curr_dir_name).parents:
    if i.name == project_name:
        absolute_project_path = i.absolute()
        break

detail_dir = os.path.join(absolute_project_path, data_dir, data_dir_bills_detailed)

# Add source for vote summary and detailed
bill_detail_meta = glob.glob(detail_dir + "/meta.csv")
detail_meta_df = pd.read_csv(bill_detail_meta[0])

det_file_lst = glob.glob(detail_dir + "/*.xml")
det_file_lst_base = [os.path.basename(x) for x in det_file_lst]

session = cf.create_session()
detail_src_obj = cf.add_sources(session,
                                [{
                                    "data_source": detail_meta_df["source_name"].to_list()[0],
                                    "date_obtained": datetime.datetime.fromisoformat(detail_meta_df["date_scraped"].to_list()[0]).date(),
                                    "misc_data": {"filenames": det_file_lst_base,
                                                  "url": detail_meta_df["source_url"].to_list()[0]}
                                }])[0]

# bill_txt_df = pd.DataFrame()
# for each_xml in det_file_lst[0:2]:
#     bill_txt_df = pd.concat([bill_txt_df, pd.read_xml(each_xml)], axis=0, ignore_index=True)

for each_xml in det_file_lst[0:2]:
    # print(file)
    file_str_mess = ""

    tree = et.parse(each_xml)
    root = tree.getroot()
    # print(root.tag)

    mp_role_dict = {}
    caucus_roles = []
    parliamentary_positions = []
    committee_member_roles = []
    association_and_group_roles = []

    for child in root:
        # print(child.tag)
        # Cover, InsideCover, MainText,
        xml_part = child.attrib.get("Part_Type")
        if xml_part == "MainText":
            for c in child:
                print(c)
                if c.tag == "Block":
                    for g_c in c:
                        if g_c.tag == "Para" or g_c.tag == "MarginalNote":
                            print(g_c)
                            if g_c.text is not None:
                                file_str_mess = file_str_mess + "\n" + g_c.text
                            if g_c.tail is not None:
                                file_str_mess = file_str_mess + "\n" + g_c.tail

                        for g_g_c in g_c:
                            print(g_g_c)
                            if g_g_c.text is not None:
                                file_str_mess = file_str_mess + "\n" + g_g_c.text
                            if g_g_c.tail is not None:
                                file_str_mess = file_str_mess + "\n" + g_g_c.tail

                            for g_g_g_c in g_g_c:
                                print(g_g_g_c)
                                if g_g_g_c.text is not None:
                                    file_str_mess = file_str_mess + "\n" + g_g_g_c.text
                                if g_g_g_c.tail is not None:
                                    file_str_mess = file_str_mess + "\n" + g_g_g_c.tail

    print("Cover")
            # for node in child:
            #     if node.tag in member_of_parliament_role_field_list:
            #         mp_role_dict[node.tag] = node.text

session.close()
print("END")
