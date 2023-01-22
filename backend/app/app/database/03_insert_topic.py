import pandas as pd
import glob
import common_func as cf
from DirectoryHandler import DirectoryHandler


def insert_topics_from_lobby_regs_comms():
    # TODO: Test on fresh db 0/1
    # TODO: Test on populated db 1/1

    # Preamble, folder locations
    dh = DirectoryHandler("lobby_regs")
    sub_csv_1 = glob.glob(dh.path_of_interest + "/*SubjectMattersExport.csv")

    dh = DirectoryHandler("lobby_comms")
    sub_csv_2 = glob.glob(dh.path_of_interest + "/*SubjectMattersExport.csv")

    sub_csv = sub_csv_1 + sub_csv_2

    if len(sub_csv) > 2 or len(sub_csv) < 2:
        raise RuntimeError("Incorrect number of csv detected.")

    session = cf.create_session(debug=True)

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

