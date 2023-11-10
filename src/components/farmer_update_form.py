import streamlit as st

import database.database as db


# Define the module
def farmer_update_form(farmer_to_update: dict):
    # Perform Data Fetching
    pcs_data = st.session_state["app_data"]["pcs_data"]
    coop_group_data = st.session_state["app_data"]["coop_group_data"]
    farmers_data = st.session_state["app_data"]["farmers_data"]

    # Define Static Values
    edu_levels = ["MSL", "JHS", "SSCE", "TERTIARY", "NFE"]
    positions = [
        "Chairperson",
        "Vice Chairperson",
        "Secretary",
        "Member",
    ]
    gender = ["M", "F"]

    with st.container():
        with st.form(key="Farmer Update Form", clear_on_submit=True):
            st.subheader(
                f"Update - {farmer_to_update['NAME OF FARMER']}", divider="green"
            )
            column1, column2, column3 = st.columns(3)

            with column1:
                farmer_name = st.text_input(
                    label="Name", value=farmer_to_update.get("NAME OF FARMER")
                )
                farmer_gender = st.selectbox(
                    label="Gender",
                    options=gender,
                    index=gender.index(farmer_to_update.get("SEX (M/F)"))
                    if farmer_to_update.get("SEX (M/F)") in gender
                    else None,
                )
                farmer_farm_size = st.text_input(
                    label="Farm Size",
                    help="Enter the Size of the Farm",
                    value=farmer_to_update.get("FARM SIZE"),
                )

            with column2:
                farmer_age = st.text_input(
                    label="Age",
                    help="Enter the Age of the Farmer",
                    value=farmer_to_update.get("AGE"),
                )
                farmer_edu_level = st.selectbox(
                    label="Farmer Education Level",
                    help="Select Farmer Education Level",
                    options=edu_levels,
                    index=edu_levels.index(farmer_to_update.get("EDU LEVEL"))
                    if farmer_to_update.get("EDU LEVEL") in edu_levels
                    else None,
                )
                farmer_cooperative = st.selectbox(
                    label="Cooperative Group",
                    help="Select Farmer Cooperative Group",
                    options=coop_group_data,
                    format_func=lambda coop: coop["NAME"],
                    index=next(
                        (
                            index
                            for index, coop in enumerate(coop_group_data)
                            if coop["NAME"] == farmer_to_update.get("COOPERATIVE GROUP")
                        ),
                        None,
                    ),
                )

            with column3:
                farmer_position = st.selectbox(
                    label="Position",
                    options=positions,
                    index=positions.index(farmer_to_update.get("EXECUTIVE POSITION"))
                    if farmer_to_update.get("EXECUTIVE POSITION") in positions
                    else None,
                )
                farmer_phone_number = st.text_input(
                    label="Contact Number", value=farmer_to_update.get("PHONE CONTACT")
                )

                farmer_pc = st.selectbox(
                    label="PC",
                    help="Select Farmer PC",
                    options=pcs_data,
                    format_func=lambda pc: pc["NAME"],
                    index=next(
                        (
                            index
                            for index, pc in enumerate(pcs_data)
                            if pc["NAME"] == farmer_to_update.get("PC")
                        ),
                        None,
                    ),
                )

            farmer = {
                "NAME OF FARMER": farmer_name,
                "SEX (M/F)": farmer_gender,
                "EXECUTIVE POSITION": farmer_position,
                "PHONE CONTACT": farmer_phone_number,
                "AGE": farmer_age,
                "COOPERATIVE GROUP": farmer_cooperative["NAME"]
                if farmer_cooperative is not None
                else None,
                "EDU LEVEL": farmer_edu_level,
                "FARM SIZE": farmer_farm_size,
                "PC": farmer_pc["NAME"] if farmer_pc is not None else None,
            }

            # Define the submit button
            update_button = st.form_submit_button(
                label="Update Farmer", use_container_width=True, type="primary"
            )

            if update_button:
                try:
                    # Update record
                    results = db.update_record(
                        collection="farmers",
                        payload=farmer,
                        id=str(farmer_to_update.get("_id")),
                    )

                    if results.acknowledged:
                        # Update farmers_data in session state
                        farmers_data = db.fetch_records(collection="farmers")
                        st.session_state["app_data"]["farmers_data"] = farmers_data

                        st.toast(
                            f":green[Successfully Updated Farmer - {str(farmer_to_update.get('_id'))}]"
                        )

                    else:
                        st.toast(":red[Update was not successful]")

                except Exception as e:
                    st.toast(f":red[Error updating farmer] - {str(e)}")
