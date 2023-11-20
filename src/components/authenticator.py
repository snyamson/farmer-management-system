import streamlit as st
import streamlit_authenticator as stauth
import yaml
import os
from yaml.loader import SafeLoader


# Determine if the code is running in production or locally
if os.getenv("ENVIRONMENT") == "production":
    # Code is running in production mode
    credentials_file_path = "/etc/secrets/credentials.yaml"
else:
    # Code is running locally
    credentials_file_path = "./credentials.yaml"

# Define the Instance of the Auth
with open(credentials_file_path) as file:
    config = yaml.load(file, Loader=SafeLoader)

authenticator = stauth.Authenticate(
    config["credentials"],
    config["cookie"]["name"],
    config["cookie"]["key"],
    config["cookie"]["expiry_days"],
    config["preauthorized"],
)


# Define the Main Auth Function
def auth():
    if st.session_state["authentication_status"] is not True:
        st.markdown(
            """
            <style>
                    header.st-emotion-cache-18ni7ap.ezrtsby2,
                    button.st-emotion-cache-11ixbc7.ef3psqc4,
                    button.st-emotion-cache-iiif1v.ef3psqc4,
                    footer.st-emotion-cache-164nlkn.ea3mdgi1 {
                        display: None;
                    }

                    @media screen and (max-width: 767px) {
                        div.st-emotion-cache-1v0mbdj.e115fcil1 {
                        margin-left: auto;
                        margin-right: auto;
                    }               
                    
            </style>
        """,
            unsafe_allow_html=True,
        )
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(
                "<h1 style='text-align: center'>BAPWAYS MANAGEMENT SYSTEM </h1>",
                unsafe_allow_html=True,
            )
            col4, col5, col6 = st.columns([1, 4, 1])
            col5.image(image="images/logo.jpg", width=300)

        with col2:
            st.markdown(f'{"<br>" * 2}', unsafe_allow_html=True)
            _, status, __ = authenticator.login("Login", "main")

            if status is None:
                st.toast("Please enter your username and password")

            if status is False:
                st.toast(":red[Username/password is incorrect]")
