import streamlit as st

from components.render_delete import render_delete


def perform_data_delete(data: str, collection: str, placeholder: str = None):
    records = st.session_state["app_data"][data]

    d_select, d_display = st.columns([2, 6])
    with d_select:
        selected_record = st.selectbox(
            label="Select Farmer to Update",
            key=data,
            options=records,
            format_func=lambda record: record["NAME OF FARMER"]
            if data == "farmers_data"
            else record["NAME"],
            index=None,
            label_visibility="collapsed",
            placeholder=placeholder if placeholder is not None else "Select Record",
        )
    with d_display:
        # Create a dictionary for faster lookup
        record_dict = {str(record["_id"]): record for record in records}
        if selected_record is not None:
            selected_record_data = record_dict.get(str(selected_record["_id"]))
            # Add the id field
            selected_record_data["_id"] = selected_record["_id"]

            # Delete Record Here
            render_delete(
                selected_data=selected_record_data, collection=collection, data=data
            )
