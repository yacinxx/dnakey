from streamlit import toast, success, snow
from license.license_manager import VERSION
import datetime

class ConfigManager:
    def __init__(self, prime_key:str) -> None:
        with open("profile_config/profile_config.json", "r") as f: 
            self.profile_data = __import__("json").loads(f.read())
        self.profile_config = self.profile_data["profiles_config"]
        self.prime_key = prime_key
        self.create_date = datetime.datetime.now()
        self.formatted_datetime = self.create_date.isoformat()

    def configuration(self):
        return self.profile_config
    
    def update_created_profiles(self):
        self.profile_config[self.prime_key]["created_profiles"] +=1
        toast(":orange[**1 Profile has been added to your prime key**]", icon="🍨")
        return self.profile_config[self.prime_key]["created_profiles"]

    def get_date_time(self):
        return self.profile_config[self.prime_key]["date_time"]

    def update_date_time(self):
        if self.profile_config[self.prime_key]["date_time"] is None:
            self.profile_config[self.prime_key].update({"date_time": self.formatted_datetime})
            success("**You 'Prime Key' has been activated successfully!**", icon="🍧")
            snow()
    
    def update_profile_activity(self, id_profile:int, activate_merge:bool, save_cookies:bool, formatted_datetime:str) -> None:
        self.action = self.profile_config[self.prime_key]["profile_activity"]["action"]
        if id_profile not in self.action:
            self.action.update({id_profile:{
                "active_usage": 0,
                "active_merge": activate_merge,
                "date_time": formatted_datetime,
                "request_status": "online",
                "save_cookies": save_cookies,
                "version": VERSION}
                })

    def get_created_profiles(self):
        return self.profile_config[self.prime_key]["created_profiles"]

    def get_active_profiles(self):
        active_profiles_ids = []
        active_profiles = 0
        active_profiles_list = list(self.profile_config[self.prime_key]["profile_activity"]["action"])
        for i in active_profiles_list:
            if self.profile_config[self.prime_key]["profile_activity"]["action"][i]["active_usage"] != 0:
                active_profiles+=1
                active_profiles_ids.append(f"id:{i}")
        return active_profiles, active_profiles_ids if len(active_profiles_ids) != 0 else ""      

    def get_online_profiles(self):
        all_profiles_online = [] 
        active_profiles_list = list(self.profile_config[self.prime_key]["profile_activity"]["action"])
        for i in active_profiles_list:
            if self.profile_config[self.prime_key]["profile_activity"]["action"][i]["request_status"] == "online":
                all_profiles_online.append("online")
            else:
                all_profiles_online.append("offline")
        if all(profile == "online" for profile in all_profiles_online):
            return "Online!"
        else:
            return "Not all profiles are online!"

    def check_active_usage(self):
        all_profiles_active_usage = []
        for i in list(self.profile_config[self.prime_key]["profile_activity"]["action"]):
            all_profiles_active_usage.append(self.profile_config[self.prime_key]["profile_activity"]["action"][i]["active_usage"])
        if all(profile == 0 for profile in all_profiles_active_usage):
            return "first_time"

    def get_profile_active_usage(self, id_profile:str) -> int:
        return self.profile_config[self.prime_key]["profile_activity"]["action"][id_profile]["active_usage"]

    def update_profile_active_usage(self, id_profile:str) -> None:
        self.profile_config[self.prime_key]["profile_activity"]["action"][id_profile]["active_usage"] +=1

    def get_merge_active_usage(self):
        return len(list(self.profile_config[self.prime_key]["profile_activity"]["action_merge"]))

    def get_profile_action_merge(self, id_profile:str) -> list[int]:
        get_merge = self.profile_config[self.prime_key]["profile_activity"]["action_merge"][id_profile]
        action_merge_len = len(list(get_merge.keys()))
        action_merge = sum(list(get_merge.values()))
        return action_merge_len, action_merge

    def update_profile_action_merge(self, id_profile:str, merge_with:str) -> None:
        action_merge = self.profile_config[self.prime_key]["profile_activity"]["action_merge"]
        if id_profile not in list(action_merge.keys()):
            action_merge.update({id_profile:{f"({id_profile},{merge_with})": 0}})
        if id_profile in list(action_merge.keys()):
            if f"({id_profile},{merge_with})" in list(action_merge[id_profile].keys()):
                action_merge[id_profile][f"({id_profile},{merge_with})"] +=1 
            else:
                action_merge[id_profile].update({f"({id_profile},{merge_with})": 0})     
                action_merge[id_profile][f"({id_profile},{merge_with})"] +=1       
    
    def update_config(self):
        with open("profile_config/profile_config.json", "w") as f:
           __import__("json").dump(self.profile_data, f, indent=3)
        