import streamlit as st
import time

import database.database as db
from styles.input_request import button_style, progress_style


# Define the module
def input_request_form():
    # Data Fetching
    coop_group_data = st.session_state["app_data"]["coop_group_data"]

    # Form Title
    st.subheader("Input Request Form", divider="green")

    # Initialize session state
    if "is_registered" not in st.session_state:
        st.session_state.is_registered = False

    # Create a 3x3 grid layout
    col1, col2, col3 = st.columns(3)

    # Types and Region
    types_options = [
        "Insecticides",
        "Fungicides",
        "Herbicides",
        "Knapsack Sprayer",
        "Mistblower Sprayer",
        "Urea Fertilizer",
        "NPK Fertilizer",
        "Sulphate of Ammonia",
    ]

    regions = [
        "Ashanti",
        "Brong-Ahafo",
        "Central",
        "Eastern",
        "Volta",
        "Western North",
        "Western South",
    ]

    with col1:
        farmer_name = st.text_input("Name")
        total_cost = st.number_input("Total Cost", min_value=0.0)

    with col2:
        selected_type = st.multiselect("Type", options=types_options)
        amount_paid = st.number_input("Amount Paid", min_value=0.0)

    with col3:
        quantity = st.number_input("Quantity", min_value=1, step=1)
        date_supplied = st.date_input("Date Supplied", value="today")

    # Check if the person is registered
    st.session_state.is_registered = st.checkbox("Is Farmer Registered?")

    # Community, District and Region
    community = ""
    district = ""
    region = ""

    if st.session_state.is_registered == False:
        col4, col5, col6 = st.columns(3)
        community = col4.text_input(label="Community")
        district = col5.text_input(label="District")
        region = col6.selectbox(label="Region", options=regions, index=None)

    # Display the name input dynamically based on registration status
    if st.session_state.is_registered:
        # If registered, ask for the cooperative name
        cooperative_name = st.selectbox(
            label="Cooperative Group",
            options=coop_group_data,
            format_func=lambda coop: coop["NAME"],
            index=None,
        )
    else:
        cooperative_name = None

    # Submit button
    submitted = st.button(
        "Submit Request",
        use_container_width=True,
    )

    # Display the captured inputs after form submission
    if submitted:
        if farmer_name == "":
            st.error("Farmer name required")
        elif st.session_state.is_registered == False and (
            region is None or district == "" or community == ""
        ):
            st.error("Please provide the demographic info of the farmer")

        else:
            button_style(state="hide")
            with st.status("Submitting Request") as status:
                input_request = {
                    "NAME": farmer_name,
                    "INPUT TYPE": selected_type,
                    "QUANTITY": quantity,
                    "DATE SUPPLIED": date_supplied.isoformat(),
                    "IS REGISTERED": st.session_state.is_registered,
                    "COOPERATIVE GROUP": cooperative_name.get("NAME")
                    if cooperative_name is not None
                    else None,
                    "TOTAL COST": total_cost,
                    "AMOUNT PAID": amount_paid,
                    "BALANCE": round((total_cost - amount_paid), 2),
                    "COMMUNITY": community
                    if community != ""
                    else cooperative_name.get("COMMUNITY"),
                    "DISTRICT": district
                    if district != ""
                    else cooperative_name.get("DISTRICT"),
                    "REGION": region
                    if region != ""
                    else cooperative_name.get("REGION"),
                }

                input_request_id = db.insert_record(
                    collection="input_requests", payload=input_request
                )

                if input_request_id is not None:
                    status.update(
                        label="Request Submitted Successfully",
                        state="complete",
                        expanded=False,
                    )
                time.sleep(3)
                progress_style()
                button_style(state="show")
