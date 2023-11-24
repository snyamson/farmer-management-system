import streamlit as st

from components.input_request_update import input_request_update


def perform_input_requests_update():
    input_requests = st.session_state["app_data"]["input_requests"]

    d_select, d_display = st.columns([2, 6])
    with d_select:
        selected_request = st.selectbox(
            label="Select Farmer Name to Update",
            options=input_requests,
            format_func=lambda input: input["NAME"],
            index=None,
            label_visibility="collapsed",
            placeholder="Select Farmer Name",
        )
    with d_display:
        # Create a dictionary for faster lookup
        request_dict = {str(input["_id"]): input for input in input_requests}
        if selected_request is not None:
            selected_request_data = request_dict.get(str(selected_request["_id"]))
            # Add the id field
            selected_request_data["_id"] = selected_request["_id"]

            # Perform Update
            input_request_update(request_to_update=selected_request_data)
