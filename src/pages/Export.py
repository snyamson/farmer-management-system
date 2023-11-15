# Import Libraries
import streamlit as st
import pandas as pd
from streamlit_extras.dataframe_explorer import dataframe_explorer


# Application Page Configuration
st.set_page_config(
    page_title="Data Export | Bapways Farmer Management",
    page_icon="./images/logo.jpg",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Import Modules and Components
import database.database as db
from components.authenticator import auth
from components.app_bar import app_bar


# Load Initial Application Data from Database
db.load_initial_app_data()

# Check for Authentication
if st.session_state["authentication_status"] is not True:
    auth()
else:
    # Data Export Page
    app_bar(title="DATA EXPORT", superuser=False)

    # Minimize the padding
    st.markdown(
        """
        <style>
            .block-container { padding-top: 2rem; padding-bottom: 2rem;}   
        </style>
        """,
        unsafe_allow_html=True,
    )

    # filtered_df = dataframe_explorer(
    #     df=pd.DataFrame(st.session_state["app_data"]["coop_group_data"])
    # )
    # st.dataframe(filtered_df, use_container_width=True)
