import streamlit as st

from components.cooperatives_update_form import cooperatives_update_form


def perform_cooperative_update():
    coop_group_data = st.session_state["app_data"]["coop_group_data"]

    d_select, d_display = st.columns([2, 6])
    with d_select:
        selected_group = st.selectbox(
            label="Select Group to Update",
            options=coop_group_data,
            format_func=lambda group: group["NAME"],
            index=None,
            label_visibility="collapsed",
            placeholder="Select Cooperative Group",
        )
    with d_display:
        # Create a dictionary for faster lookup
        group_dict = {str(group["_id"]): group for group in coop_group_data}
        if selected_group is not None:
            selected_group_data = group_dict.get(str(selected_group["_id"]))
            # Add the id field
            selected_group_data["_id"] = selected_group["_id"]

            # Update Cooperative Group here
            cooperatives_update_form(coop_group_to_update=selected_group_data)
