import streamlit as st
from create_profile import CreateProfile
from create_password import CreatePassword
from feedbacks.send_feedbacks import Feedbacks
from license.license_manager import CO_FOUNDER, VERSION

# Set Streamlit page configuration
st.set_page_config(
    page_title="Dnakey",
    page_icon="🔐",
    layout="centered",
)

class App(CreateProfile, CreatePassword, Feedbacks):
    def start_dnakey(self):
        self.display_text_header()
        tab1, tab2, tab3 = st.tabs(["Create Profile", "Create Password", "Feedback"])
        with tab1:
            self.new_profile()
        with tab2:
            if self.hash_key and self.tab_name:
                st.subheader("**_You can't use this tab yet!_**", divider="gray")
                st.caption(f"**_If you wanna create the password please remove the prime key from (:green[{self.tab_name}])_**", 
                           help="For Security Purposes")
            else:
                self.create_new_password()            
        with tab3:
            if self.hash_key and self.tab_name:
                st.subheader("**_You can't use this tab yet!_**", divider="gray")
                st.caption(f"**_If you wanna send a feedback please remove the prime key from (:green[{self.tab_name}])_**", 
                           help="For Security Purposes")
            else:
                self.feedbacks()   

    def display_text_header(self):
        st.title(f"DnaKey-Beta (*V{VERSION}*)")
        st.caption(f"**Programmer by: {CO_FOUNDER}**")
        st.caption("**Get Your Prime Key**: https://yassinesallami.gumroad.com/l/nrbjx")
        st.caption("**My LinkedIn**: https://www.linkedin.com/in/yassinesallami1/")
        st.caption("**_Description_**: **DnaKey** is a simple service that allows you to create more complex password using a simple key-word!")   
        st.caption("Donate: [ **_:orange[hixvmx] - :orange[4$]_** ]")

if __name__ == '__main__':
    # Start the app
    App().start_dnakey()
