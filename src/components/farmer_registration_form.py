import streamlit as st

import database.database as db

# Define the module
def farmer_registration_form():
    # Perform Data Fetching
    pcs_name_id = st.session_state["app_data"]["pcs_name_id"]
    coop_group_name_id = st.session_state["app_data"]["coop_group_name_id"]

    # Define the Name Options for SelectBoxes
    pcs_options = [pc["NAME"] for pc in pcs_name_id]
    coop_options = [coop["NAME"] for coop in coop_group_name_id]

    with st.container():
        with st.form(key="Farmer Data Entry", clear_on_submit=True):
            st.subheader("Farmer Registration Form", divider="green")
            column1, column2, column3 = st.columns(3)

            with column1:
                farmer_name = st.text_input(label="Name of Farmer")
                farmer_gender = st.selectbox(label="Gender", options=["M", "F"])
                farmer_farm_size = st.text_input(
                    label="Farm Size", help="Enter the Size of the Farm"
                )

            with column2:
                farmer_age = st.text_input(
                    label="Age of Farmer",
                    help="Enter the Age of the Farmer",
                )
                farmer_edu_level = st.selectbox(
                    label="Farmer Education Level",
                    help="Select Farmer Education Level",
                    options=["MSL", "JHS", "SSCE", "TERTIARY", "NFE"],
                )
                farmer_cooperative = st.selectbox(
                    label="Cooperative Group",
                    help="Select Farmer Cooperative Group",
                    options=coop_options,
                )

            with column3:
                farmer_position = st.selectbox(
                    label="Position",
                    options=[
                        "Chairperson",
                        "Vice Chairperson",
                        "Secretary",
                        "Member",
                    ],
                )
                farmer_phone_number = st.text_input(label="Contact Number")

                farmer_pc = st.selectbox(
                    label="PC",
                    help="Select Farmer PC",
                    options=pcs_options,
                )

            farmer = {
                "NAME OF FARMER": farmer_name,
                "SEX (M/F)": farmer_gender,
                "EXECUTIVE POSITION": farmer_position,
                "PHONE CONTACT": farmer_phone_number,
                "AGE": farmer_age,
                "COOPERATIVE GROUP": farmer_cooperative,
                "EDU LEVEL": farmer_edu_level,
                "FARM SIZE": farmer_farm_size,
                "PC": farmer_pc,
            }

            # Define the submit button
            submit_button = st.form_submit_button(use_container_width=True)

            if submit_button:
                try:
                    # Insert record
                    farmer_id = db.insert_record(collection="farmers", payload=farmer)

                    # Update farmers_data in session state
                    st.session_state["app_data"]["farmers_data"] = db.fetch_records(
                        collection="farmers"
                    )

                    st.toast(f":green[Successfully added farmer - {farmer_id}]")
                except Exception as e:
                    st.toast(":red[Error adding farmer")