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
from components.authenticator import auth
from components.pc_registration_form import pc_registration_form
from components.farmer_registration_form import farmer_registration_form
from components.cooperatives_registration_form import cooperatives_registration_form


# Load Initial Application Data from Database
db.load_initial_app_data()

# Check for Authentication
if st.session_state['authentication_status'] is not True:
    auth()
else:
    # Home Page
    manage_users_button = app_bar(title='DATA ENTRY', superuser=True if st.session_state['name'] == 'Solomon Nyamson' else False)

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
        st.write('Manage Users on this tab')

    else:
        # Set up the tabs for the various forms 
        pcs_tab, farmers_tab, cooperatives_tab, agric_inputs_tab, cocoa_records_tab = st.tabs(
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
            pc_registration_form()

        # Farmers Registration Form
        with farmers_tab:
            farmer_registration_form()

        # Cooperatives Registration Form
        with cooperatives_tab:
            cooperatives_registration_form()