import streamlit as st
import json, time, re
from cryptography.fernet import Fernet
from prime_key_config import PrimeKeyConfig
from profile_config.config_manager import ConfigManager
from main_builder import MainBuilder
from create_merge import *

class CreatePassword(PrimeKeyConfig):
    def create_new_password(self):
        key_id = "prime-key-password"
        self.hash_key = st.text_input("Enter Your Prime Key: (:red[Required])", 
                                      type="password", 
                                      help="Prime Key is your login token method so 'DnaKey' can recognize you!", 
                                      key=key_id)
        self.upload_hash_key = self.agent_prime_key(self.hash_key)
        if self.upload_hash_key == 1:
            self.tab_name = "Create Password"
            return
        else:
            self.tab_name = "Create Password"
            self.config_has_key = f"dnakey${self.upload_hash_key[:32:2]}"
            self.config_manager = ConfigManager(self.config_has_key)  
            self.config_manager.update_date_time()
            self.config_manager.update_config()
            self.first_time = self.config_manager.check_active_usage()                      
            self.col3, self.col4 = st.columns(2)
            with self.col3:
                if self.first_time == "first_time":
                    st.info("Hey there. It's look like your first time using your profile!", icon="🏁")
                with st.expander("Upload Profile [See More...]"):
                    self.uploaded_file = st.file_uploader(label="Upload Profile",
                                                        help="Required a dkp file only!",
                                                        accept_multiple_files=True,
                                                        type=["dkp"], key="file-01",
                                                        label_visibility="collapsed")                
                self.profile_data()          
                self.uploaded_files_merge = self.uploaded_file
                self.create_password_advance_settings()
            with self.col4:    
                if self.first_time == "first_time":
                    st.success("Let me help you get your first password easily!", icon="⚙") 
                if not self.uploaded_file:
                    st.caption("Hello👋, To start creating your new password you need to upload your profile!")
                if (self.uploaded_file) and (self.first_time == "first_time"):
                    st.info("**_Active Profile For Now_**: Here you have to select the profile that you wanna use!", icon="🛠")  
            self.input_for_user_key()
            self.decode_text_button()             

    def profile_data(self):
        if not self.uploaded_file:
            return 1
        self.create_a_fernet_object()
        self.verify_uploaded_file()

    def create_a_fernet_object(self):
        # Create a Fernet object with the secret key
        secret_key = self.upload_hash_key.encode("utf-8")
        self.fernet = Fernet(secret_key)

    def verify_uploaded_file(self):
        self.uploaded_file_unpack = []
        for file in range(len(self.uploaded_file)):
            encrypted_data = self.uploaded_file[file].read().decode("utf-8")
            try:
                decrypted_data = self.fernet.decrypt(encrypted_data)
                decrypted_string = decrypted_data.decode()
                self.data = json.loads(decrypted_string)
                self.uploaded_file_unpack.append(self.data)
            except Exception:
                with self.col4:
                    invalid_profile_name = self.uploaded_file[file].name[:-4].replace('dnakey_', '')
                    st.error(f"This is not a dnakey profile! '{invalid_profile_name}'")
                    time.sleep(0.5)
                    st.info("If you don't know you can create a 'dnakey' profile in 'Create Profile window' in your left!", icon="ℹ️")
                    st.stop() 
        if len(self.uploaded_file_unpack) == 1:
            st.toast("**:green[The Profile Data Is Live...]**", icon="🍰") 
            time.sleep(1)
        else:
            st.toast("**:blue[Your Profiles Data Is Live...]**", icon="🍬") 
            time.sleep(1)

    def create_password_advance_settings(self):
        if self.uploaded_file and self.upload_hash_key:
            if self.first_time == "first_time":
                st.info("**_Advance Settings_**: Here you have the Merge it's an advanced method. You won't need it for now!", icon="🧪")  
            with st.expander("Advance Settings [See More...]"):               
                self.new_merge_profile = CreateMergeProfile(self.uploaded_file_unpack, self.uploaded_files_merge)
                self.new_merge_profile.merge_builder()
                st.caption(":red[Warning]: The profiles must have the same length!")
            if self.first_time == "first_time":
                st.warning("**_Activate Random_**: If you activate this it gonna give you a temporary random password!", icon="⚠") 
            self.activate_random_on = st.toggle("Activate Random: (:green[Optional])")

    def select_file_option(self):
        MAX_UPLOADS = 11
        self.uploaded_length = len(self.uploaded_file)
        merge_options_name_length = len(self.new_merge_profile.merge_options_name)
        is_disabled = False if merge_options_name_length < 1 and self.uploaded_length != 1 else True
        if (self.uploaded_file) and (self.upload_hash_key) and (self.uploaded_length < MAX_UPLOADS):
            self.file_names_options = [self.uploaded_file[i].name[:-4].replace('dnakey_', '') for i in range(self.uploaded_length)] 
            self.options = st.selectbox("Active Profile For Now: (:green[Live..])", (self.file_names_options), disabled=is_disabled)
            if self.options: 
                for j in range(self.uploaded_length):
                    if self.options == self.file_names_options[j]:
                        return self.uploaded_file_unpack[j]
        else:
            st.error("You can't upload more than 10 profile at once!", icon='🚨')
            exit()

    def input_for_user_key(self):
        if not self.uploaded_file:
            return 1
        with self.col4:
            self.uploaded_file = self.select_file_option()
            max_length_input = self.uploaded_file.get("meta_data", {}).get("profile_length", None) // 4
            if self.first_time == "first_time":
                st.info("**_Enter Your Key_**: Here you can enter a sample word to encode it to a complex password!", icon="🧬")  
            self.key_input = st.text_input("Enter Your Key: (:red[Required])", 
                                                max_chars=max_length_input,
                                                placeholder="Example: Blue / Cat...",
                                                type="password", 
                                                key="input-00")
            if self.first_time == "first_time":
                st.warning("**_Warning_**: You have to remember the word that you entered here!", icon="⚠")         
            if not self.key_input:
                return 1
            self.check_input_for_user_key()

    def check_input_for_user_key(self):
        valid_pattern = re.compile("^[a-zA-Z0-9]+$")
        if valid_pattern.search(self.key_input):
            self.key_input = self.key_input
            get_profile_name = self.uploaded_file.get("meta_data", {}).get("profile_name", None)
            get_request_status = self.uploaded_file.get("meta_data", {}).get("request_status", None)
            if not self.new_merge_profile.merge_options_name:
                st.toast(f"**:orange[Profile {get_profile_name} Is {get_request_status}...]**", icon="🍕")
                time.sleep(1)
        else:
            st.caption(":red[Warning]: If you don't know 'Dnakey' dont support (**symbols or empty spaces!**)")
            self.key_input = None 

    def decode_text_button(self):
        if not self.uploaded_file:
            return 1
        is_disabled = True if not self.key_input else False
        create_password_button = st.button("Create Password!", disabled=is_disabled, key=1)
        if create_password_button:
            self.decode_profile_data()                    

    def decode_profile_data(self):
        self.key_input_list = self.key_input.strip()
        if self.key_input:
            if (self.uploaded_file) and (not self.new_merge_profile.merge_options_name):
                self.data = self.uploaded_file
            elif (self.uploaded_file) and (self.new_merge_profile.merge_options_name):
                self.data = self.new_merge_profile.profile_data_merge
            valid_hash_key = f"dnakey${self.upload_hash_key[:32:2]}"
            main_builder = MainBuilder(valid_hash_key, self.data)
            main_builder.dna_builder(self.key_input_list, self.activate_random_on)
