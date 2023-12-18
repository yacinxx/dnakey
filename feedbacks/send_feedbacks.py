import streamlit as st
from prime_key_config import PrimeKeyConfig
from profile_config.config_manager import ConfigManager
import datetime, json

class Feedbacks(PrimeKeyConfig):
    def __init__(self):
        with open("feedbacks/feedbacks_config.json", "r") as f:
                self.feedback_data = json.loads(f.read())

    def feedbacks(self):
        key_id = "prime-key-feedback"
        self.hash_key = st.text_input("Enter Your Prime Key: (:red[Required])", 
                                      type="password", 
                                      help="Prime Key is your login token method so 'DnaKey' can recognize you!", 
                                      key=key_id)
        self.hash_key_feedback = self.agent_prime_key(self.hash_key)
        if self.hash_key_feedback != 1:
            self.config_has_key = f"dnakey${self.hash_key_feedback[:32:2]}"
            self.config_manager = ConfigManager(self.config_has_key) 
            self.config_manager.update_date_time()
            self.config_manager.update_config()
            self.send_feedback_form()
            self.check_feedback_prime_key()
            self.display_feedback_result()
            self.get_feedbacks()

    def send_feedback_form(self):
        with st.form("send_feedback", clear_on_submit=True):
            st.write("Send Feedback!")
            self.user_feedback = st.text_area("Please Enter Your feedback: (:red[Required])", 
                                              max_chars=300, 
                                              placeholder="You can leave your feedback here!")
            self.user_rate = st.multiselect("Rate This with: (:green[Optional])", 
                                            options=["🔐🔐🔐", "🔐🔐🔐🔐", "🔐🔐🔐🔐🔐"], 
                                            default="🔐🔐🔐🔐🔐", 
                                            max_selections=1)
            self.submitted = st.form_submit_button("Submit")

    def display_feedback_result(self):
        if self.user_feedback and self.submitted:
            with st.chat_message("user"):  
                st.write("Your Feedback!")                  
                st.text(self.user_feedback)
                self.user_rate = f"Rate: {self.user_rate.index(0)}" if self.user_rate else ""
                st.text(self.user_rate)

    def check_feedback_prime_key(self):
        self.feedback_has_key = f"dnakey${self.hash_key_feedback[:32:2]}"
        if (self.submitted) and (self.feedback_has_key in list(self.feedback_data.get("feedbacks").keys())):
           st.info("You are already send as you feedback!")
           exit()

    def get_feedbacks(self):
        if self.user_feedback and self.submitted:
            create_date = datetime.datetime.now()
            formatted_datetime = create_date.isoformat()
            feedback_data = {
                "user_feedback": self.user_feedback, 
                "user_rate": (len(self.user_rate)-6), 
                "date_time": formatted_datetime
                }
            self.feedback_data.get("feedbacks").update({self.feedback_has_key: feedback_data})
            with open("feedbacks/feedbacks_config.json", "w") as f:
                json.dump(self.feedback_data, f, indent=3)
