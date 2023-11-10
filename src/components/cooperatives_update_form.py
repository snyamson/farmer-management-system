import streamlit as st
from datetime import datetime

import database.database as db


# Define the module
def cooperatives_update_form(coop_group_to_update: dict):
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
        with st.form(key="Cooperative Group Update Form", clear_on_submit=True):
            st.subheader(
                f"Update - {coop_group_to_update.get('NAME')}", divider="green"
            )
            column1, column2 = st.columns(2)

            with column1:
                group_name = st.text_input(
                    label="Name",
                    help="Cooperative Group Name",
                    value=coop_group_to_update.get("NAME"),
                )
                group_district = st.text_input(
                    label="District",
                    help="Cooperative Group District",
                    value=coop_group_to_update.get("DISTRICT"),
                )
                group_community = st.text_input(
                    label="Community of Operation",
                    help="Community Cooperative Group of Operation",
                    value=coop_group_to_update.get("COMMUNITY"),
                )

            with column2:
                group_region = st.selectbox(
                    label="Region",
                    help="Select Cooperative Group Region",
                    options=region,
                    index=region.index(coop_group_to_update.get("REGION"))
                    if coop_group_to_update.get("REGION") in region
                    else None,
                )
                group_pc = st.selectbox(
                    label="Cooperative PC",
                    help="Select Cooperative Group PC",
                    options=pcs_data,
                    format_func=lambda pc: pc["NAME"],
                    index=next(
                        (
                            index
                            for index, pc in enumerate(pcs_data)
                            if pc["NAME"] == coop_group_to_update.get("PC")
                        ),
                        None,
                    ),
                )
                group_date_registered = st.date_input(
                    label="Date Registered",
                    help="Date of group registration",
                    value=datetime.strptime(
                        coop_group_to_update["DATE OF REGISTRATION"], "%Y-%m-%d"
                    ),
                )

                cooperative_group = {
                    "NAME": group_name,
                    "DISTRICT": group_district,
                    "COMMUNITY": group_community,
                    "REGION": group_region,
                    "DATE OF REGISTRATION": group_date_registered.isoformat(),
                    "PC": group_pc["NAME"] if group_pc is not None else None,
                }

            cooperative_update_button = st.form_submit_button(
                label="Update Cooperative Group",
                use_container_width=True,
                type="primary",
            )

            if cooperative_update_button:
                try:
                    results = db.update_record(
                        collection="cooperative_groups",
                        payload=cooperative_group,
                        id=str(coop_group_to_update.get("_id")),
                    )

                    if results.acknowledged:
                        # Update coop_group_data in session state
                        coop_group_data = db.fetch_records(
                            collection="cooperative_groups"
                        )
                        st.session_state["app_data"][
                            "coop_group_data"
                        ] = coop_group_data
                        st.toast(
                            f":green[Successfully Updated Group - {coop_group_to_update.get('_id')}]"
                        )
                    else:
                        st.toast(":red[Update was not successful]")

                except Exception as e:
                    st.toast(f":red[Error updating group - {str(e)}]")
