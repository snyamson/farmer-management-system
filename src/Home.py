# Import Libraries
import streamlit as st
from datetime import date
from datetime import datetime

# Application Page Configuration
st.set_page_config(
    page_title="Data Entry | Bapways Farmer Management",
    page_icon="./images/logo.jpg",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Import Modules and Components
import database.database as db
from components.app_bar import app_bar
from components.authenticator import auth
from components.pc_registration_form import pc_registration_form
from components.pc_update_form import pc_update_form
from components.farmer_registration_form import farmer_registration_form
from components.cooperatives_registration_form import cooperatives_registration_form


# Load Initial Application Data from Database
db.load_initial_app_data()

# Check for Authentication
if st.session_state["authentication_status"] is not True:
    auth()
else:
    # Home Page
    manage_users_button = app_bar(
        title="DATA ENTRY",
        superuser=True if st.session_state["name"] == "Solomon Nyamson" else False,
    )

    # Minimize the padding
    st.markdown(
        """
        <style>
            .block-container { padding-top: 2rem; padding-bottom: 2rem;}   
        </style>
        """,
        unsafe_allow_html=True,
    )

    if manage_users_button:
        b_col1, b_col2 = st.columns([1, 5])
        b_col1.button(label="Back")

    else:
        pcs_name_id = st.session_state["app_data"]["pcs_name_id"]
        pcs_options = [pc for pc in pcs_name_id]
        pcs_data = st.session_state["app_data"]["pcs_data"]
        # Set up the tabs for the various forms
        (
            pcs_tab,
            farmers_tab,
            cooperatives_tab,
            agric_inputs_tab,
            cocoa_records_tab,
        ) = st.tabs(
            [
                "PURCHASING CLERKS (PCs)",
                "FARMERS",
                "COOPERATIVE GROUPS",
                "FARMER INPUTS",
                "COCOA RECORDS",
            ]
        )

        # PCs Registration Form
        with pcs_tab:
            pc_add, pc_update, pc_delete = st.tabs(["ADD", "EDIT", "DELETE"])
            with pc_add:
                pc_registration_form()
            with pc_update:
                d_select, d_display = st.columns([2, 6])
                with d_select:
                    selected_pc = st.selectbox(
                        label="Select PC to Update",
                        options=pcs_options,
                        format_func=lambda pc: pc["NAME"],
                        index=None,
                    )
                with d_display:
                    # Create a dictionary for faster lookup
                    pcs_dict = {str(pc["_id"]): pc for pc in pcs_data}
                    if selected_pc is not None:
                        selected_pc_data = pcs_dict.get(selected_pc["_id"])
                        # Add the id field
                        selected_pc_data["_id"] = selected_pc["_id"]

                        # Update PC here
                        pc_update_form(pc_to_update=selected_pc_data)

                       

        # Farmers Registration Form
        with farmers_tab:
            farmer_registration_form()

        # Cooperatives Registration Form
        with cooperatives_tab:
            cooperatives_registration_form()
