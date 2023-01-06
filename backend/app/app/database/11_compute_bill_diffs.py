import datetime
import glob
import os
import pathlib
import pandas as pd
import common_func as cf
import xml.etree.ElementTree as et
from sqlmodel import select
from schema_creation.sqlmodel_build import (Bill, LegStage)


def get_all_para_marginalnotes_xml(xml_elem):
    mini_mess = []
    for c in xml_elem:
        # if c.tag == "Block":
        #     mini_mess += get_all_para_marginalnotes_xml(c)
        # else:

        #if c.tag == "Para" or c.tag == "MarginalNote":
        if c.text is not None:
            mini_mess = mini_mess + [c.text]
        if c.tail is not None:
            mini_mess = mini_mess + [c.tail]

        mini_mess += get_all_para_marginalnotes_xml(c)

    return mini_mess


# Preamble, folder locations
project_name = "app"  # collide\backend\app\app
data_dir = "data"
data_dir_bills_detailed = os.path.join("bills", "debug")

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
bill_dict = {}
xml_reading_map = {
    "first-reading-senate": 1,
    "first-reading-house": 1,
    "second-reading-senate": 2,
    "second-reading-house": 2,
    "report-house": 2,
    "third-reading-senate": 3,
    "third-reading-house": 3,
    "assented-to": 4
}

stat = select(LegStage)
all_stages = session.exec(stat).all()
legstage_map = {}
for each_leg_stage in all_stages:
    if each_leg_stage.match_name == "housereadingfirst":
        legstage_map["first-reading-house"] = each_leg_stage.id
    if each_leg_stage.match_name == "housereadingsecond":
        legstage_map["second-reading-house"] = each_leg_stage.id
        legstage_map["report-house"] = each_leg_stage.id
    if each_leg_stage.match_name == "housereadingthird":
        legstage_map["third-reading-house"] = each_leg_stage.id
    if each_leg_stage.match_name == "senatereadingfirst":
        legstage_map["first-reading-senate"] = each_leg_stage.id
    if each_leg_stage.match_name == "senatereadingsecond":
        legstage_map["second-reading-senate"] = each_leg_stage.id
    if each_leg_stage.match_name == "senatereadingthird":
        legstage_map["third-reading-senate"] = each_leg_stage.id
    if each_leg_stage.match_name == "royalassent":
        legstage_map["assented-to"] = each_leg_stage.id

stat = select(Bill)
all_bills = session.exec(stat).all()

# TODO: computer diffs for every combination
# TODO: create billdiff objects, insert into table

for idx, each_bill in enumerate(all_bills):
    print(f"Bill loop {idx} of {len(all_bills)}")
    match_id = each_bill.id
    uc_match_name = each_bill.match_name.upper()
    match_file_lst = glob.glob(detail_dir + f"/{uc_match_name}_*.xml")

    if len(match_file_lst) > 0:
        bill_dict[match_id] = {}

    for jdx, each_xml in enumerate(match_file_lst):
        print(f"XML loop {jdx} of {len(match_file_lst)}")
        # print(file)
        file_str_mess = []

        tree = et.parse(each_xml)
        root = tree.getroot()
        bill_name = root.attrib.get("Bill_No")
        bill_reading = root.attrib.get("Stage_Name")
        # print(root.tag)

        file_name_info = os.path.basename(each_xml).split("_")
        expected_parl = int(file_name_info[0])
        expected_parl_session = int(file_name_info[1])
        expected_bill_name = file_name_info[2]
        expected_reading = int(file_name_info[3].split(".")[0])

        for child in root:
            # print(child.tag)
            # Cover, InsideCover, MainText,
            if child.tag == "Identification":
                for g_c in child:
                    if g_c.tag == "BillNumber":
                        bill_name = g_c.text
                    if g_c.tag == "BillHistory":
                        for g_g_c in g_c:
                            if g_g_c.tag == "Stages":
                                bill_reading = g_g_c.attrib.get("stage")
            xml_part = child.attrib.get("Part_Type")
            if xml_part == "MainText" or child.tag == "Body":
                file_str_mess += get_all_para_marginalnotes_xml(child)

        file_str_mess = '\n'.join(file_str_mess)
        print(file_str_mess)

        # sanity check filename vs file contents
        if bill_name.lower() == expected_bill_name.lower():
            if xml_reading_map.get(bill_reading.lower()) == expected_reading:
                bill_dict[match_id][legstage_map.get(bill_reading.lower())] = file_str_mess
            else:
                raise AssertionError("Reading number does not match")
        else:
            raise AssertionError("Bill number does not match")


session.close()
print("END")
