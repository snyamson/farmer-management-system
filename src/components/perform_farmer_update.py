import streamlit as st

from components.farmer_update_form import farmer_update_form


def perform_farmer_update():
    farmers_data = st.session_state["app_data"]["farmers_data"]

    d_select, d_display = st.columns([2, 6])
    with d_select:
        selected_farmer = st.selectbox(
            label="Select Farmer to Update",
            options=farmers_data,
            format_func=lambda farmer: farmer["NAME OF FARMER"],
            index=None,
            label_visibility="collapsed",
            placeholder="Select Farmer",
        )
    with d_display:
        # Create a dictionary for faster lookup
        farmer_dict = {str(farmer["_id"]): farmer for farmer in farmers_data}
        if selected_farmer is not None:
            selected_farmer_data = farmer_dict.get(str(selected_farmer["_id"]))
            # Add the id field
            selected_farmer_data["_id"] = selected_farmer["_id"]

            # Update Farmer here
            farmer_update_form(farmer_to_update=selected_farmer_data)
