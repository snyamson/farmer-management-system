# Import Libraries
import streamlit as st

# Application Page Configuration
st.set_page_config(
    page_title='Data Entry | Bapways Farmer Management',
    page_icon="./images/logo.jpg",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Import Modules and Components
import database.database as db
from components.app_bar import app_bar


# Load Initial Application Data from Database
if "app_data" not in st.session_state:
    # Cooperative Groups (Names and IDs Only)
    coop_group_name_id = db.fetch_names_and_ids(collection="cooperative_groups")
    # Cooperative Groups
    coop_group_data = db.fetch_records(collection="cooperative_groups")
    # PC (Names and IDs Only)
    pcs_name_id = db.fetch_names_and_ids(collection="pcs")
    # PCs
    pcs_data = db.fetch_records(collection="pcs")
    # Farmers
    farmers_data = db.fetch_records(collection="farmers")

    # Update session state with the new data
    st.session_state["app_data"] = {
        "coop_group_name_id": coop_group_name_id,
        "coop_group_data": coop_group_data,
        "pcs_name_id": pcs_name_id,
        "pcs_data": pcs_data,
        "farmers_data": farmers_data,
    }

# Home Page
app_bar(title='Data Entry')

# Set up the tabs for the various forms 
