import streamlit as st

import database.database as db

# Define the module
def cooperatives_registration_form():
    # Perform Data Fetching
    pcs_name_id = st.session_state["app_data"]["pcs_name_id"]

    # Define the Name Options for SelectBoxes
    pcs_options = [pc["NAME"] for pc in pcs_name_id]

    with st.container():
        with st.form(key="Cooperative Group Data Entry", clear_on_submit=True):
            st.subheader("Cooperative Group Registration Form", divider="green")
            column1, column2 = st.columns(2)

            with column1:
                group_name = st.text_input(label="Name", help="Cooperative Group Name")
                group_district = st.text_input(
                    label="District", help="Cooperative Group District"
                )
                group_community = st.text_input(
                    label="Community of Operation",
                    help="Community Cooperative Group of Operation",
                )

            with column2:
                group_region = st.selectbox(
                    label="Region",
                    help="Select Cooperative Group Region",
                    options=[
                        "Ashanti",
                        "Brong-Ahafo",
                        "Central",
                        "Eastern",
                        "Volta",
                        "Western North",
                        "Western South",
                    ],
                )
                group_pc = st.selectbox(
                    label="Cooperative PC",
                    help="Select Cooperative Group PC",
                    options=pcs_options,
                )
                group_date_registered = st.date_input(
                    label="Date Registered", help="Date of group registration"
                )

                cooperative_group = {
                    "NAME": group_name,
                    "DISTRICT": group_district,
                    "COMMUNITY": group_community,
                    "REGION": group_region,
                    "DATE OF REGISTRATION": group_date_registered.isoformat(),
                    "PC": group_pc,
                }

            cooperative_submit_button = st.form_submit_button(
                label="Submit", use_container_width=True
            )

            if cooperative_submit_button:
                try:
                    group_id = db.insert_record(
                        collection="cooperative_groups", payload=cooperative_group
                    )

                    # Update coop_group_data and coop_group_name_id in session state
                    coop_group_name_id = db.fetch_names_and_ids(
                        collection="cooperative_groups"
                    )
                    coop_group_data = db.fetch_records(
                        collection="cooperative_groups"
                    )
                    st.session_state["app_data"]["coop_group_name_id"] = coop_group_name_id
                    st.session_state["app_data"]["coop_group_data"] = coop_group_data
                    st.toast(f":green[Successfully added group - {group_id}]")
                except Exception as e:
                    st.toast(f":red[Error adding group - {str(e)}]")