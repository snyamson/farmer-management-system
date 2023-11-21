# Import Libraries
import streamlit as st
from streamlit_extras.switch_page_button import switch_page
from streamlit_extras.metric_cards import style_metric_cards
from streamlit_extras.stylable_container import stylable_container
from streamlit_extras.row import row


# Application Page Configuration
st.set_page_config(
    page_title="Home | Bapways Farmer Management",
    page_icon="./images/logo.jpg",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Import Modules and Components
import database.database as db
from components.app_bar import app_bar
from components.authenticator import auth
from styles.styles_main import container_style


# Load Initial Application Data from Database
db.load_initial_app_data()

# Check for Authentication
if st.session_state["authentication_status"] is not True:
    auth()
else:
    # Home Page
    manage_users_button = app_bar(
        title="BAPWAYS MANAGEMENT SYSTEM",
        superuser=True if st.session_state["username"] == "bapways_admin" else False,
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

    # Card styling
    style_metric_cards(box_shadow=False, border_left_color="#067528")

    # Company Information
    with stylable_container(key="info_container", css_styles=container_style):
        image, info = st.columns([2, 4])

        # Center the Image on Mobile
        st.markdown(
            """
            <style>
                
                @media screen and (max-width: 767px) {
                        div.st-emotion-cache-1v0mbdj.e115fcil1 {
                            margin-left: auto;
                            margin-right: auto;
                        }
                    }  
                    
            </style>

            """,
            unsafe_allow_html=True,
        )

        # Add Logo
        with image:
            st.image("./images/logo.jpg")

        # Add Information
        with info:
            st.markdown(
                "<p style='font-size: 1rem; text-align: justify; margin-top: auto; margin-bottom: auto; line-height: 2;'>BAPWAYS Agri Solutions GH Ltd. is a farmer-centered agribusiness that aims to address the challenges faced by smallholder cassava and cocoa farmers, particularly women farmers in Ghana. Our mission is to improve the livelihoods of smallholder cassava farmers by providing comprehensive support, including quality inputs, labor, financial inclusion, and training on Best Agronomic Practices (BAP). </p>",
                unsafe_allow_html=True,
            )

    # Main Statistics

    st.subheader("CURRENT STATISTICS")
    tag1, tag2, tag3, tag4 = st.columns(4)
    tag1.metric(
        label="TOTAL FARMERS",
        value=(len(st.session_state["app_data"]["farmers_data"])),
    )

    tag2.metric(
        label="TOTAL COOPERATIVES",
        value=(len(st.session_state["app_data"]["coop_group_data"])),
    )

    tag3.metric(
        label="TOTAL PURCHASING CLERKS",
        value=(len(st.session_state["app_data"]["pcs_data"])),
    )

    tag4.metric(
        label="TOTAL INPUT REQUESTS",
        value=len(st.session_state["app_data"]["input_requests"]),
    )

    # Go To Buttons
    with stylable_container(
        key="buttons_container",
        css_styles=container_style,
    ):
        st.subheader("GO TO")
        button1, button2, button3 = st.columns([1, 1, 5])
        with button1:
            if st.button(
                label="Perform Data Entry",
            ):
                switch_page("Data Entry")

        with button2:
            if st.button(
                label="Explore Data",
            ):
                switch_page("Explore")
