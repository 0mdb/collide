import pandas as pd
import glob
import common_func as cf
from DirectoryHandler import DirectoryHandler


def insert_topics_from_lobby_regs_comms(debug_status):
    # Preamble, folder locations
    dh_reg = DirectoryHandler("lobby_regs")
    sub_csv_1 = glob.glob(dh_reg.path_of_interest + "/*SubjectMattersExport.csv")

    dh_comms = DirectoryHandler("lobby_comms")
    sub_csv_2 = glob.glob(dh_comms.path_of_interest + "/*SubjectMattersExport.csv")

    sub_csv = sub_csv_1 + sub_csv_2

    if len(sub_csv) > 2 or len(sub_csv) < 2:
        raise RuntimeError("Incorrect number of csv detected.")

    session = cf.create_session(debug=debug_status)

    # Add sources
    dh_reg.load_meta_file()
    objs = cf.add_sources(session, [{"data_source": dh_reg.source_name,
                                     "date_obtained": dh_reg.source_age,
                                     "misc_data": dh_reg.source_misc}])
    dh_comms.load_meta_file()
    objs = cf.add_sources(session, [{"data_source": dh_comms.source_name,
                                     "date_obtained": dh_comms.source_age,
                                     "misc_data": dh_comms.source_misc}])

    for each_file in sub_csv:
        df = pd.read_csv(each_file)
        subs = df["SUBJ_MATTER_OBJET"].to_list()

        try:
            subs = subs + df["OTHER_SUBJ_MATTER_AUTRE_OBJET"].to_list()
            print("Other subject exists")
        except:
            print("No other subject exists")

        i = 0

        subs_unique = list(set(subs))

        for itm in subs_unique:
            print(f"{i} of {len(subs_unique)}")
            cf.add_commstopic(session, [{"topic_display_name": str(itm)}])
            i = i + 1

    session.close()
    print("\tcompleted topics")

