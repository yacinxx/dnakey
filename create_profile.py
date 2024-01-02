import streamlit as st
import pandas as pd
import time
import enginev2
from prime_key_config import PrimeKeyConfig
from profile_config.config_manager import ConfigManager

class CreateProfile(PrimeKeyConfig):
    def new_profile(self):
        key_id = "prime-key-profile"
        self.hash_key = st.text_input("Enter Your Prime Key: (:red[Required])", 
                                      type="password", 
                                      help="Prime Key is your login token method so 'DnaKey' can recognize you!", 
                                      key=key_id)
        self.create_hash_key = self.agent_prime_key(self.hash_key)
        if self.create_hash_key == 1:
            self.tab_name = "Create Profile"
            return  
        else:
            self.tab_name = "Create Profile"
            self.config_has_key = f"dnakey${self.create_hash_key[:32:2]}"
            self.config_manager = ConfigManager(self.config_has_key)
            self.config_manager.update_date_time()
            self.config_manager.update_config()
            self.col_new_profile1, self.col_new_profile2 = st.columns(2)
            self.created_profiles = self.config_manager.get_created_profiles()
            with self.col_new_profile1:
                self.profile_name_settings()
                self.activate_merge = st.toggle("Activate Merge: (:blue[Advance])", 
                                                value=True, 
                                                help="[:red[WARNING]]: If you turn it off you can't merge this profile with a other!")     
                st.caption(":red[WARNING]: If you turn it off you can't merge this profile with a other!")
            with self.col_new_profile2:
                if self.created_profiles < 1:
                    st.warning("**_Caution_**: Refrain from implementing DnaKey in real-life accounts as it remains in an experimental phase, and its reliability and security have not been fully validated.", 
                               icon="❕")
                self.new_profile_advance_settings()
                self.save_cookies = st.toggle("Save Cookies: (:green[For Better Performance])", 
                                              value=True, 
                                              help="With save cookies 'dnakey' can track prime key activity and show you all the info about it and whose use it!")   
                st.caption("**:orange[Security Tracking]**: If you turn it off 'DnaKey' can't give you good result!")     
            self.create_new_profile()

    def profile_name_settings(self):
        if self.created_profiles < 1:
                    st.info("Welcome to DnaKey. We are glad you wanna test it!", icon="🎉")
        with st.expander("Profile Settings! [See More...]", expanded=True):
            if self.created_profiles < 1:
                st.info("You can start with given your profile a name!", icon="🍿")
            self.create_profile_name()
            if self.created_profiles > 1:
                self.options_profile_name = st.selectbox("Choose Options: (:red[Experimental])", ["One Profile"], disabled=True)
                st.caption(":blue[Info]: This option under the test (not stable!)")
            else:
                self.options_profile_name = "One Profile"

    def create_profile_name(self):
        self.profile_name = st.text_input("Profile Name: (:red[Required])", 
                                        placeholder="Example: Emails...",
                                        key='profile_name')
        st.caption(":green[Note]: You can't change your profile name later!")

    def new_profile_advance_settings(self):
        with st.expander("Advance Settings! [See More...]"):
            if self.created_profiles < 1:
                st.info("This is the Advanced profile settings you don't have to mess with this yet!", icon="⚙")
            self.length_slider = st.slider("Enter Max Length: (:green[Optional])", min_value=4, max_value=20, value=10, step=2)
            st.caption(":green[Note]: The Max Length leave it in (:blue[default mode 10])")
            self.has_choice = st.multiselect("Password Includes: (:green[Optional])",
                                        options=["Lowercase","Uppercase","Numbers","Symbols", "Arabic"],
                                        default=["Lowercase","Uppercase","Numbers"])
            if self.has_choice:
                self.lowercase = True if "Lowercase" in self.has_choice else False
                self.uppercase = True if "Uppercase" in self.has_choice else False
                self.numbers = True if "Numbers" in self.has_choice else False
                self.symbols = True if "Symbols" in self.has_choice else False
                self.arabic = True if "Arabic" in self.has_choice else False        

    def create_new_profile(self):
        is_disabled = True if not self.profile_name else False
        create_new_profile = st.button("Create New Profile", disabled=is_disabled, key=0)
        if( create_new_profile) and (self.profile_name != ""):
            if self.options_profile_name == "One Profile":
                empty_input = "profile"
                self.profile_list(empty_input)
            elif self.options_profile_name == "Multi":
                empty_input = "profiles"
                self.lst_profile_name = self.profile_name.split(",")
                for profile in self.lst_profile_name:
                    self.profile_name  = profile
                    self.profile_list(empty_input)

    def profile_list(self, empty_input:str) -> None:
        my_bar = st.progress(0, text=f"Creating {empty_input} please wait...")
        for percent_complete in range(100):
            time.sleep(0.01)
            my_bar.progress(percent_complete + 1, text=f"Creating {empty_input} please wait...")
        time.sleep(1)
        my_bar.empty()                
        self.check_brain_data()                
        st.toast(f"**:green[The new {empty_input} created successfully!]**", icon='🎉')
        time.sleep(1)                
                
    def check_brain_data(self):
        self.engine = enginev2.DNAEngine
        param_for_engine = {
                "has_key": self.create_hash_key,
                "profile_name": self.profile_name,
                "length": self.length_slider * 4,
                "activate_merge": self.activate_merge,
                "save_cookies": self.save_cookies,
                "has_lower": self.lowercase,
                "has_upper": self.uppercase,
                "has_number": self.numbers,
                "has_symbol": self.symbols,
                "has_arabic": self.arabic,
            }
        # Create a new instance of MainBuilder engine
        new_profile = self.engine(**param_for_engine)
        # Write the Dnakey profile to a file
        self.encrypted_profile_contents, self.profile_contents = new_profile.create_dnakey_profile()
        # Display a download button for the brain data file
        st.divider()
        self.download_profile_data()

    def download_profile_data(self):
        if self.options_profile_name == "One Profile":
            self.date_time = self.profile_contents.get("meta_data", {}).get("date_time", None)
            self.profile_version = self.profile_contents.get("meta_data", {}).get("version", None)
            self.profile_id = self.profile_contents.get("meta_data", {}).get("profile_id", None)
            self.request_status = self.profile_contents.get("meta_data", {}).get("request_status", None)
            self.profile_result()
            with st.expander("You can see your profile details before download it! [See More...]"):
                incol1, incol2 = st.columns(2)
                with incol1:
                    self.profile_meta_data()
                with incol2:
                    self.profile_includes()
                    self.prime_key_meta_data()
        elif self.options_profile_name == "Multi Profiles" and len(self.lst_profile_name) > 2:
            st.code(self.encrypted_profile_contents.decode("utf-8"))

    def profile_result(self):
        col1, col2 = st.columns(2)
        with col1:
            st.write("Download Profile: (:red[Required])")
            st.download_button(label='Download Data As DKP',
                                    data=self.encrypted_profile_contents,
                                    file_name=f'dnakey_{self.profile_name}.dkp')
            st.caption(":green[Note]: You have to download the profile to use it in 'Create Password Tab'")                    
        with col2:
            st.write("Copy Profile Content: (:green[Optional])")
            st.text(self.encrypted_profile_contents.decode("utf-8"))
            st.caption(":red[WARNING]: Create a file with (:blue[.dkp]) in the end!")

    def profile_meta_data(self):
        st.text("Profile MetaData!")
        profile_meta_data = ['profile_id', 'profile_name', 'length', 'profile_quantity', 'activate_merge', 'save_cookies', 'request_status','date_time', 'version']
        profile_values = [self.profile_id, self.profile_name, self.length_slider, 'One Profile', self.activate_merge, self.save_cookies, self.request_status, self.date_time, self.profile_version]
        self.create_profile_data_frame(profile_meta_data, profile_values)

    def profile_includes(self):
        st.text("Profile Includes!")
        st.code(f"""
                has_lower = {self.lowercase}
                has_upper = {self.uppercase}
                has_number = {self.numbers}
                has_symbol = {self.symbols}
                has_arabic = {self.arabic}""")

    def prime_key_meta_data(self):
        st.text("PrimeKey MetaData!")
        active_profiles, active_profiles_ids = self.config_manager.get_active_profiles()
        st.code(f"""
                prime_key_id: '{self.config_has_key}'
                created_profiles: {self.created_profiles}
                active_profiles: {active_profiles} {active_profiles_ids}
                profiles_status: '{self.config_manager.get_online_profiles()}'
                date_time: '{self.config_manager.get_date_time()}'""")

    def create_profile_data_frame(self, profile_meta_data:list[str], profile_values:list[str | int | bool]) -> None:
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
