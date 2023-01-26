import glob
import pandas as pd
import common_func as cf
import json
from DirectoryHandler import DirectoryHandler


def insert_bills():
    # TODO: Test on fresh db 0/1
    # TODO: Test on populated db 1/1

    # Preamble, folder locations
    dh_bills = DirectoryHandler("bills summary")
    dh_bills.load_meta_file()

    bills_json = glob.glob(dh_bills.path_of_interest + "/*.json")

    if len(bills_json) > 1:
        raise RuntimeError("More than one json detected.")

    session = cf.create_session(debug=True)
    src_obj = cf.add_sources(session, [{"data_source": dh_bills.source_name,
                                        "date_obtained": dh_bills.source_age,
                                        "misc_data": dh_bills.source_misc}])[0]

    # Construct list of bills
    with open(bills_json[0], encoding="utf-8") as f:
        data = f.read()
        structure = json.loads(data)

    bills_df = pd.json_normalize(structure)

    bill_name = bills_df["NumberCode"].to_list()
    parl = bills_df["ParliamentNumber"].to_list()
    parl_sess = bills_df["SessionNumber"].to_list()
    desc = bills_df["LongTitleEn"].to_list()
    house_bool = bills_df["IsHouseBill"].to_list()
    senate_bool = bills_df["IsSenateBill"].to_list()
    first_house_read_date = bills_df["PassedHouseFirstReadingDateTime"].to_list()
    second_house_read_date = bills_df["PassedHouseSecondReadingDateTime"].to_list()
    third_house_read_date = bills_df["PassedHouseThirdReadingDateTime"].to_list()
    first_senate_read_date = bills_df["PassedSenateFirstReadingDateTime"].to_list()
    second_senate_read_date = bills_df["PassedSenateSecondReadingDateTime"].to_list()
    third_senate_read_date = bills_df["PassedSenateThirdReadingDateTime"].to_list()
    royal_assent_date = bills_df["ReceivedRoyalAssentDateTime"].to_list()

    print(f"Expected entry count: {len(bill_name)}")

    bill_lst = []
    for idx, every_bill in enumerate(bill_name):
        bill_lst.append({"bill_name": every_bill,
                         "parliament": parl[idx],
                         "parliament_session": parl_sess[idx],
                         "description": desc[idx],
                         "is_house_bill": house_bool[idx],
                         "is_senate_bill": senate_bool[idx],
                         "first_house_read_date": first_house_read_date[idx],
                         "second_house_read_date": second_house_read_date[idx],
                         "third_house_read_date": third_house_read_date[idx],
                         "first_senate_read_date": first_senate_read_date[idx],
                         "second_senate_read_date": second_senate_read_date[idx],
                         "third_senate_read_date": third_senate_read_date[idx],
                         "royal_assent_date": royal_assent_date[idx],
                         "source_id": src_obj.id})

    bills_objs = cf.add_bills(session, bill_lst)

    session.close()
