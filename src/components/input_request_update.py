import streamlit as st
import time
from datetime import datetime

import database.database as db
from styles.input_request import button_style, progress_style


# Define the module
def input_request_update(request_to_update: dict):
    # Data Fetching
    coop_group_data = st.session_state["app_data"]["coop_group_data"]

    # Form Title
    st.subheader(
        f"Update Request for - {request_to_update.get('NAME')}", divider="green"
    )

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
        farmer_name = st.text_input(
            "Name", key="update_name", value=request_to_update.get("NAME")
        )
        total_cost = st.number_input(
            "Total Cost",
            key="update_total_cost",
            min_value=0.0,
            value=request_to_update.get("TOTAL COST"),
        )

    with col2:
        selected_type = st.multiselect(
            "Type",
            options=types_options,
            key="update_type",
            default=request_to_update.get("INPUT TYPE"),
        )
        amount_paid = st.number_input(
            "Amount Paid",
            min_value=0.0,
            key="update_amt_paid",
            value=request_to_update.get("AMOUNT PAID"),
        )

    with col3:
        quantity = st.number_input(
            "Quantity",
            min_value=1,
            step=1,
            key="update_qty",
            value=request_to_update.get("QUANTITY"),
        )
        date_supplied = st.date_input(
            "Date Supplied",
            key="update_date",
            value=datetime.strptime(request_to_update.get("DATE SUPPLIED"), "%Y-%m-%d"),
        )

    # Check if the person is registered
    st.session_state.is_registered = st.checkbox(
        "Is Farmer Registered?",
        key="update_reg",
        value=request_to_update.get("IS REGISTERED"),
    )

    # Community, District and Region
    community = ""
    district = ""
    region = ""

    if st.session_state.is_registered == False:
        col4, col5, col6 = st.columns(3)
        community = col4.text_input(
            label="Community",
            key="update_com",
            value=request_to_update.get("COMMUNITY"),
        )
        district = col5.text_input(
            label="District", key="update_dist", value=request_to_update.get("DISTRICT")
        )
        region = col6.selectbox(
            label="Region",
            options=regions,
            key="update_region",
            index=regions.index(request_to_update.get("REGION"))
            if request_to_update.get("REGION") in region
            else None,
        )

    # Display the name input dynamically based on registration status
    if st.session_state.is_registered:
        # If registered, ask for the cooperative name
        cooperative_name = st.selectbox(
            label="Cooperative Group",
            options=coop_group_data,
            format_func=lambda coop: coop["NAME"],
            key="update_coop",
            index=next(
                (
                    index
                    for index, group in enumerate(coop_group_data)
                    if group["NAME"] == request_to_update.get("COOPERATIVE GROUP")
                ),
                None,
            ),
        )
    else:
        cooperative_name = None

    # Submit button
    submitted = st.button(
        "Update Input Request",
        use_container_width=True,
        key="update_btn",
        type="primary",
    )

    # Declare the Empty loader
    loading = st.empty()

    # Display the captured inputs after form submission
    if submitted:
        if farmer_name == "":
            st.error("Farmer name required")
        elif st.session_state.is_registered == False and (
            region is None or district == "" or community == ""
        ):
            st.error("Please provide the demographic info of the farmer")

        else:
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
                "REGION": region if region != "" else cooperative_name.get("REGION"),
            }

            if submitted:
                loading = st.info("Updating..")
                try:
                    results = db.update_record(
                        collection="input_requests",
                        payload=input_request,
                        id=str(request_to_update.get("_id")),
                    )

                    if results.acknowledged:
                        # Update the data
                        st.session_state["app_data"][
                            "input_requests"
                        ] = db.fetch_records(collection="input_requests")
                        # Remove the loader
                        loading.empty()

                        st.toast(
                            f":green[Successfully updated request id - {request_to_update.get('_id')}]"
                        )

                except Exception as e:
                    loading.empty()
                    st.toast(f":red[Failed updating request - {str(e)}]")
