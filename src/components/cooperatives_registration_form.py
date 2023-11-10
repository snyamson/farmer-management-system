import streamlit as st

import database.database as db


# Define the module
def cooperatives_registration_form():
    # Perform Data Fetching
    pcs_data = st.session_state["app_data"]["pcs_data"]

    # Define Static Values
    region = [
        "Ashanti",
        "Brong-Ahafo",
        "Central",
        "Eastern",
        "Volta",
        "Western North",
        "Western South",
    ]

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
                    options=region,
                    index=None,
                )
                group_pc = st.selectbox(
                    label="Cooperative PC",
                    help="Select Cooperative Group PC",
                    options=pcs_data,
                    format_func=lambda pc: pc["NAME"],
                    index=None,
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
                    "PC": group_pc["NAME"] if group_pc is not None else None,
                }

            cooperative_submit_button = st.form_submit_button(
                label="Submit", use_container_width=True
            )

            if cooperative_submit_button:
                try:
                    group_id = db.insert_record(
                        collection="cooperative_groups", payload=cooperative_group
                    )
                    # Update coop_group_data in session state
                    coop_group_data = db.fetch_records(collection="cooperative_groups")
                    st.session_state["app_data"]["coop_group_data"] = coop_group_data
                    st.toast(f":green[Successfully added group - {group_id}]")
                except Exception as e:
                    st.toast(f":red[Error adding group - {str(e)}]")
