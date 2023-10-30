import streamlit as st

# Application Page Configuration
st.set_page_config(
    page_title='Data Explorer | Bapways Farmer Management',
    page_icon="./images/logo.jpg",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Import Modules and Components
from components.app_bar import app_bar
from components.data_explorer import data_explorer
from utils.override_padding import override_padding

# Data Explorer Page
app_bar(title='Data Explorer')

# Minimize the padding 
st.markdown(
        """
    <style>
        .block-container { padding-top: 2rem; padding-bottom: 2rem;}   
    </style>
    """,
        unsafe_allow_html=True,
    )

# Define the Tabs
pcs_tab, farmers_tab, cooperatives_tab = st.tabs(
        ["PURCHASING CLERKS (PCs)", "FARMERS", "COOPERATIVE GROUPS"]
    )



# PCs Data Explorer
with pcs_tab:
    data_explorer(record='pcs_data', collection='pcs', column_config={
                "_id": None,
                "PC IMAGE": st.column_config.ImageColumn("PC IMAGE"),
                "G1 IMAGE": st.column_config.ImageColumn("G1 IMAGE"),
                "G2 IMAGE": st.column_config.ImageColumn("G2 IMAGE"),
                "PC SIGNED AGREEMENT": st.column_config.LinkColumn(),
            })

# Farmers Data Explorer
with farmers_tab:
    data_explorer(record='farmers_data', collection='farmers', column_config={'_id': None})

# Cooperative Groups Data Explorer
with cooperatives_tab:
    data_explorer(record='coop_group_data', collection='cooperative_groups', column_config={'_id': None})