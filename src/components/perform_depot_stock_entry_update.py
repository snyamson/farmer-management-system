import streamlit as st

from components.depot_stock_update_form import depot_stock_update_form


def perform_depot_stock_entry_update():
    depot_stock_control = st.session_state["app_data"]["depot_stock_control"]

    d_select, d_display = st.columns([2, 6])
    with d_select:
        selected_stock = st.selectbox(
            label="Select Stock to Update",
            options=depot_stock_control,
            format_func=lambda stock: stock["WAYBILL NUMBER"],
            index=None,
            label_visibility="collapsed",
            placeholder="Select WayBill Number",
        )
    with d_display:
        # Create a dictionary for faster lookup
        stock_dict = {str(stock["_id"]): stock for stock in depot_stock_control}
        if selected_stock is not None:
            selected_stock_data = stock_dict.get(str(selected_stock["_id"]))
            # Add the id field
            selected_stock_data["_id"] = selected_stock["_id"]

            # Perform Stock Update
            depot_stock_update_form(stock_to_update=selected_stock_data)
