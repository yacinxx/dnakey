import streamlit as st
import pandas as pd
from profile_config.config_manager import ConfigManager
import string, random, time
import os, qrcode

class MainBuilder:
    def __init__(self, valid_hash_key:str, data:dict) -> None:
        self.valid_hash_key = valid_hash_key
        self.config_manager = ConfigManager(self.valid_hash_key)
        self.created_profiles = self.config_manager.get_created_profiles()
        self.data = data
        self.profile_brain = self.data.get("profile_brain", {})
        self.profile_name = self.data.get("meta_data", {}).get("profile_name", None)
        self.action_status = self.data.get("meta_data", {}).get("action_status", None)
        self.length = self.data.get("meta_data", {}).get("profile_length", None)
        self.profile_id = self.data.get("meta_data", {}).get("profile_id", None)
        self.activate_merge = self.data.get("meta_data", {}).get("activate_merge", None)
        self.request_status = self.data.get("meta_data", {}).get("request_status", None)
        self.save_cookies = self.data.get("meta_data", {}).get("save_cookies", None)
        self.date_time = self.data.get("meta_data", {}).get("date_time", None)
        self.profile_version = self.data.get("meta_data", {}).get("version", None)
        self.profile_id_str = str(self.profile_id)
        self.length_convert = self.length // 4
        self.hash_text, self.prompt_list = [], []
        if self.action_status is not None:
            self.merge_with = self.data.get("meta_data", {}).get("merge_with", None)    

    def dna_builder(self, prompt:str, activate_random_on:bool) -> str:
        self.prompt = prompt
        self.numbers = [str(number) for number in string.digits]
        idx, idx_add_on = 0, 4
        for letter in prompt:
            if letter.isupper() or letter in self.numbers:
                self.hash_text.append(self.profile_brain[letter][0] 
                              ["number" if letter in self.numbers else "upper"][idx : idx + idx_add_on])
            else:
                self.hash_text.append(self.profile_brain[letter.upper()][0]["lower"][idx : idx + idx_add_on])
            idx += idx_add_on
        if activate_random_on:
            self.random_result()
        else:
            self.result_prompt()

    def random_result(self):
        if self.action_status is None:
            self.config_manager.update_profile_active_usage(self.profile_id_str)
            self.config_manager.update_config() 
        else:
            self.config_manager.update_profile_action_merge(self.profile_id_str, self.merge_with)
            self.config_manager.update_config() 
        hash_length = len(self.hash_text)
        condition = ["Weak", "#ffa347"] if hash_length < 4 else ["Medium", "#3cb371"] \
                    if hash_length < 10 else ["Strong", "#ec002b"]
        r_hash = self.create_random_result()
        _hash = ''.join(self.hash_text)
        hash_text_len = len(_hash)
        _token = f"{_hash[::4]}-{r_hash[: hash_text_len - 4]}"
        st.divider()
        with st.expander("Expand for random password result [See More...]"):
            self.col1, self.col2 = st.columns(2)
            with self.col1:
                st.write("Password: (:green[Copy])")
                st.code(f'"{_token}"')
                st.caption(f"Activate_key: {self.prompt}")
                st.caption(":red[Warning]: This is a random password (:blue[temporarily])")
        self.profile_details()
        # Generate and display QR code
        with self.col2:
            self.qr_code(_token, condition[1])
            self.hash_text.clear()       

    def create_random_result(self):
        def has_lower():
            return random.choice(string.ascii_lowercase)

        def has_upper():
            return random.choice(string.ascii_uppercase)

        def has_number():
            return random.choice(string.digits)
        
        _char = {"lower": has_lower, 
                 "upper": has_upper, 
                 "number": has_number}
        r_hash = ""
        for _ in range(self.length):
            random_choice = random.choice(list(_char.keys()))
            r_hash += _char[random_choice]()
        return r_hash

    def result_prompt(self):  
        if self.action_status is None:
            self.config_manager.update_profile_active_usage(self.profile_id_str)
            self.config_manager.update_config()  
        else:
            self.config_manager.update_profile_action_merge(self.profile_id_str, self.merge_with)
            self.config_manager.update_config() 
        jhash = ''.join(self.hash_text)
        hash_length = len(self.hash_text)
        condition = ["Weak", "#ffa347", "orange"] if hash_length < 4 else ["Medium", "#3cb371", "green"] \
                    if hash_length < 10 else ["Strong", "#ec002b", "red"]
        # Display the generated token as code
        st.divider()
        with st.expander("Expand for password result [See More...]"):
            self.col1, self.col2 = st.columns(2)
            with self.col1:
                st.write("Password: (:green[Copy])")
                st.code(f'"{jhash}"')
                st.caption(f"Condition: [:{condition[2]}[{condition[0]}]]")
                st.caption(":green[Note]: You dont have to save this password just remember your key")
        self.profile_details()      
        with self.col2:  
            # Generate and display QR code
            self.qr_code(jhash, condition[1])
        self.hash_text.clear() 
    
    def profile_details(self):
        with st.expander("Expand to see your 'Profile' Details [See More...]"):
            self.col_details1, self.col_details2 = st.columns(2)
            with self.col_details1:
                if self.action_status is None:
                    active_usage = self.config_manager.get_profile_active_usage(self.profile_id_str)
                    st.text("Profile MetaData!")         
                    profile_meta_data = ['profile_id', 'profile_name', 'active_usage', 'max_length', 'profile_status', 'activate_merge', 'save_cookies', 'date_time', 'version']
                    profile_values = [self.profile_id, self.profile_name, active_usage, self.length_convert, self.request_status, self.activate_merge, self.save_cookies, self.date_time, self.profile_version]
                    self.profile_data_frame(profile_meta_data, profile_values)
                else:  
                    merge_with, action_merge = self.config_manager.get_profile_action_merge(self.profile_id_str)
                    st.text("Profile Merge MetaData!")  
                    action_merge_name = f'{action_merge} times' if action_merge != 1 else f'{action_merge} time'
                    merge_with_name = f'{merge_with} profiles' if merge_with != 1 else f'{merge_with} profile'
                    profile_meta_data = ['profile_id', 'profile_name', 'action_merge', 'merge_with', 'max_length']
                    profile_values = [self.profile_id, self.profile_name, action_merge_name, merge_with_name, self.length_convert]
                    self.profile_data_frame(profile_meta_data, profile_values)
            with self.col_details2:
                    st.text("PrimeKey MetaData!")
                    active_profiles, active_profiles_ids = self.config_manager.get_active_profiles()
                    active_profiles_merge = self.config_manager.get_merge_active_usage()
                    profiles_status = self.config_manager.get_online_profiles()
                    st.code(f"""
                            prime_key_id: '{self.valid_hash_key}'
                            created_profiles: {self.created_profiles}
                            active_profiles: {active_profiles} {active_profiles_ids}
                            active_profiles_merge: {active_profiles_merge}
                            profiles_status: '{profiles_status}'""")     
                    st.info("Here is your profile and prime key metadata. You can save in by download it or copy the text just to be updated!", icon="❕")           
                    st.warning("DnaKey not responsible if you delete your profiles or give it to someone!", icon="📛")    

    def profile_data_frame(self, profile_meta_data:list[str], profile_values:list[str | int | bool]) -> None:
        def load_data():
            return pd.DataFrame(
                {
                    "Profile MetaData": profile_meta_data,
                    "Profile Values": profile_values,
                }
            )  
        # Boolean to resize the dataframe, stored as a session state variable
        data_df = load_data()
        data_df['Profile Values'] = data_df['Profile Values'].astype(str)
        st.dataframe(data_df, use_container_width=500, hide_index=True) 

    def qr_code(self, data_qr:str, color:str) -> None:
        # File name for the generated QR code image
        self.file_name = "qr_code.png"
        # Text to be encoded in the QR code
        qr_data_text = f"-TOKEN: {data_qr}"
        # Generate the QR code image
        self.generate_qr_code(qr_data_text, self.file_name, color)
        # Display the generated QR code image
        st.image(image=self.file_name)
        st.caption(f"You can scan this **:green[QR code]** to see your password in your phone faster!")
        st.toast(":green[Your (QR) code has been created successfully!]", icon='🎉')
        time.sleep(1)
        # Check if the image file exists
        if os.path.exists(self.file_name):
            # Delete the image file
            os.remove(self.file_name)
            print(f"Deleted the image file: {self.file_name}")
        else:
            print(f"The image file does not exist: {self.file_name}")

    def generate_qr_code(self, data:str, file_name:str, color:str) -> None:
        # Generate a QR code with the given data, file name, and color
        qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, 
                           box_size=5, border=2)
        qr.add_data(data)
        qr.make(fit=True)
        self.qr_img = qr.make_image(fill_color=color, back_color="#f5f5f5")
        # Save the generated QR code image to a file
        self.qr_img.save(file_name)