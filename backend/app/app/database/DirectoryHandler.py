import os
import shutil
import pathlib
import pandas as pd
import json


class DirectoryHandler:

    def __init__(self, dir_of_interest):
        self.source_age = None
        self.source_name = None
        self.source_misc = None

        # Preamble, folder locations
        project_name = "app"  # collide\backend\app\app

        # Folder creation, directories
        curr_dir_name = os.path.dirname(__file__)

        absolute_project_path = None
        for i in pathlib.Path(curr_dir_name).parents:
            if i.name == project_name:
                absolute_project_path = i.absolute()
                break

        self.path_project = absolute_project_path
        self.path_data = os.path.join(self.path_project, "data")
        self.dir_of_interest = dir_of_interest

        if dir_of_interest == "bills detail":
            self.path_of_interest = os.path.join(self.path_data, "bills", "detail")
        elif dir_of_interest == "bills diffs":
            self.path_of_interest = os.path.join(self.path_data, "bills", "diffs")
        elif dir_of_interest == "bills diffs_myers":
            self.path_of_interest = os.path.join(self.path_data, "bills", "diffs_myers")
        elif dir_of_interest == "bills summary":
            self.path_of_interest = os.path.join(self.path_data, "bills", "summary")
        elif dir_of_interest == "cabinet_xml":
            self.path_of_interest = os.path.join(self.path_data, "cabinet_xml")
        elif dir_of_interest == "corp_board":
            self.path_of_interest = os.path.join(self.path_data, "corp_board")
        elif dir_of_interest == "corp_no":
            self.path_of_interest = os.path.join(self.path_data, "corp_no")
        elif dir_of_interest == "ecanada_contrib":
            self.path_of_interest = os.path.join(self.path_data, "ecanada_contrib")
        elif dir_of_interest == "lobby_comms":
            self.path_of_interest = os.path.join(self.path_data, "lobby_comms")
        elif dir_of_interest == "lobby_regs":
            self.path_of_interest = os.path.join(self.path_data, "lobby_regs")
        elif dir_of_interest == "members_xml links":
            self.path_of_interest = os.path.join(self.path_data, "members_xml", "links")
        elif dir_of_interest == "members_xml member_xml":
            self.path_of_interest = os.path.join(self.path_data, "members_xml", "member_xml")
        elif dir_of_interest == "prov_ab":
            self.path_of_interest = os.path.join(self.path_data, "prov_ab")
        elif dir_of_interest == "votes detail":
            self.path_of_interest = os.path.join(self.path_data, "votes", "detail")
        elif dir_of_interest == "votes summary":
            self.path_of_interest = os.path.join(self.path_data, "votes", "summary")
        elif dir_of_interest == "wiki_tsx":
            self.path_of_interest = os.path.join(self.path_data, "wiki_tsx")
        else:
            raise AssertionError("DirectoryHandler: invalid dir_of_interest")

    def load_meta_file(self):
        meta_filename = "meta.csv"
        meta_df = pd.read_csv(os.path.join(self.path_of_interest, meta_filename))
        # self.source_age = datetime.datetime.fromisoformat(meta_df["date_scraped"].to_list()[0]).date()
        self.source_age = meta_df["date_scraped"].to_list()[0]  # string
        self.source_name = meta_df["source_name"].to_list()[0]
        self.source_misc = json.loads(meta_df["misc_data"].to_list()[0])

    def file_existing(self):
        str_age = self.source_age.split('T')[0].replace('-', '')
        target_dir = os.path.join(self.path_of_interest, str_age)

        if not os.path.exists(target_dir):
            os.makedirs(target_dir)

        file_n_dir_names = os.listdir(self.path_of_interest)
        file_names = [f for f in file_n_dir_names if os.path.isfile(os.path.join(self.path_of_interest, f))]

        for each_file in file_names:
            shutil.move(os.path.join(self.path_of_interest, each_file), os.path.join(target_dir, each_file))

    def create_meta_file(self, source_date, source_name, source_dict):
        meta_filename = "meta.csv"
        meta_path = os.path.join(self.path_of_interest, meta_filename)
        meta_df = pd.DataFrame().from_dict({
            "date_scraped": [source_date],
            "source_name": [source_name],
            "misc_data": [source_dict]
        })
        meta_df.to_csv(meta_path)