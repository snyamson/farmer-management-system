import streamlit as st

def perform_farmer_update():
    farmers_data = st.session_state['app_data']['farmers_data']

    d_select, d_display = st.columns([2, 6])
    with d_select:
                    selected_farmer = st.selectbox(
                        label="Select Farmer to Update",
                        options=farmers_data,
                        format_func=lambda farmer: farmer["NAME OF FARMER"],
                        index=None,
                        label_visibility='collapsed',
                        placeholder="Select Farmer"
                    )
    with d_display:
                    # Create a dictionary for faster lookup
                    farmer_dict = {str(farmer["_id"]): farmer for farmer in farmers_data}
                    if selected_farmer is not None:
                        selected_farmer_data = farmer_dict.get(selected_farmer["_id"])
                        # Add the id field
                        selected_farmer_data["_id"] = selected_farmer["_id"]

                        st.write(selected_farmer_data)

                        # Update Farmer here
                        # pc_update_form(pc_to_update=selected_pc_data)