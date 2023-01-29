import pandas as pd
import glob
import common_func as cf
from DirectoryHandler import DirectoryHandler

# https://ised-isde.canada.ca/site/corporations-canada/en/data-services#1
# No source/no meta loading


def insert_sector_industry_from_tsx_listing(debug_status):
    # TODO: Test on fresh db 0/1
    # TODO: Test on populated db 1/1

    # Preamble, folder locations
    dh = DirectoryHandler("wiki_tsx")
    tsx_csv = glob.glob(dh.path_of_interest + "/*comp_index_tsx.csv")

    if len(tsx_csv) > 1 or len(tsx_csv) < 1:
        raise RuntimeError("Incorrect number of csv detected.")

    df = pd.read_csv(tsx_csv[0])
    sectors = df["section"].to_list()
    industries = df["industry"].to_list()

    session = cf.create_session(debug=debug_status)

    # Insert tsx source although nothing currently uses id
    dh.load_meta_file()
    tsx_source_objs = cf.add_sources(session, [{"data_source": dh.source_name,
                                                "date_obtained": dh.source_age,
                                                "misc_data": dh.source_misc}])

    for idx, itm in enumerate(sectors):
        sect_obj = cf.add_sectors(session, [{"sector_name": sectors[idx],
                                             "industry_name": industries[idx]}])

    session.close()
