from streamlit import multiselect, toast, error
import merge
import time

class CreateMergeProfile:
    def __init__(self, uploaded_file_unpack:list[dict], uploaded_files_merge:object) -> None:
        self.merge = merge.Merge
        self.uploaded_file_unpack = uploaded_file_unpack
        self.uploaded_files_merge = uploaded_files_merge

    def merge_options(self):
        self.uploaded_length = len(self.uploaded_files_merge)
        is_disabled = True if self.uploaded_length < 2 else False
        self.merge_options_list = [f"{self.uploaded_files_merge[i].name[:-4].replace('dnakey_', '')} (Merge On)" if self.uploaded_file_unpack[i]["meta_data"]["activate_merge"] == True else f"{self.uploaded_files_merge[i].name[:-4].replace('dnakey_', '')} (Merge Off)" for i in range(self.uploaded_length)]
        self.merge_options_name = multiselect("Merge Profiles: (:red[Experimental])",
                                            self.merge_options_list,
                                            max_selections=2,
                                            placeholder="Choose 2 Profiles!",
                                            disabled=is_disabled)

    def merge_builder(self):
        self.merge_options()
        if self.merge_options_name and len(self.merge_options_name) == 2: 
            for i in range(self.uploaded_length):
                if self.merge_options_name[0] == self.merge_options_list[i]:
                    profile_1 = self.uploaded_file_unpack[i]
                elif self.merge_options_name[1] == self.merge_options_list[i]:
                    profile_2 = self.uploaded_file_unpack[i]
            merge_valid_1 = profile_1["meta_data"]["activate_merge"]
            merge_valid_2 = profile_2["meta_data"]["activate_merge"]
            if (merge_valid_1 == False) or (merge_valid_2 == False):
                error("**:orange[You can't merge blocked profiles!]**", icon='🔑')
                time.sleep(1)
                exit()
            elif self.merge(profile_1, profile_2).get_merge_error() == 1:
                error("**:orange[You can't merge 2 profiles that don't have the same length!]**", icon='🔑')
                time.sleep(1)
                exit()
            else:
                self.profile_data_merge = self.merge(profile_1, profile_2).merge_brain()
                toast("**:green[The Profiles Merge Successfully]**", icon='🍭')
                time.sleep(1)