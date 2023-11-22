import streamlit as st
from time import sleep

import database.database as db


# Define Module
def depot_stock_control_form():
    # Perform Data Fetching
    pcs_data = st.session_state["app_data"]["pcs_data"]

    with st.form(key="Depot Stock Control Entry Form", clear_on_submit=True):
        # Form Title
        st.subheader("Depot Stock Control Form", divider="green")

        col1, col2, col3 = st.columns(3)

        with col1:
            entry_date = st.date_input(label="Date")

        with col2:
            waybill_number = st.text_input(label="WayBill Number")

        with col3:
            society = st.text_input(label="Society")

        pc = st.selectbox(
            label="PC",
            options=pcs_data,
            format_func=lambda pc: pc["NAME"],
            index=None,
        )

        with st.container():
            st.subheader("Primary Evacuation")
            col4, col5 = st.columns(2)

            with col4:
                pri_bag = st.number_input(label="Bag", min_value=0, key="pri_bag")

            with col5:
                pri_cumulative = st.number_input(
                    label="Cumulative", min_value=0, key="pri_cum"
                )

        with st.container():
            st.subheader("Secondary Evacuation")
            col6, col7 = st.columns(2)

            with col6:
                sec_bag = st.number_input(label="Bag", min_value=0, key="sec_bag")

            with col7:
                sec_cumulative = st.number_input(
                    label="Cumulative", min_value=0, key="sec_cum"
                )

        balance = st.number_input(label="Balance", min_value=0, key="balance")

        submit_button = st.form_submit_button(label="Submit", use_container_width=True)

    # Stock Data
    stock = {
        "DATE": entry_date.isoformat(),
        "WAYBILL NUMBER": waybill_number,
        "SOCIETY": society,
        "PC": pc.get("NAME") if pc is not None else None,
        "PRI-EVAC: BAG": pri_bag,
        "PRI-EVAC: CUMULATIVE": pri_cumulative,
        "SEC-EVAC: BAG": sec_bag,
        "SEC-EVAC: CUMULATIVE": sec_cumulative,
        "BALANCE": balance,
    }
    # Declare the Empty loader
    loading = st.empty()

    if submit_button:
        loading = st.info("Submitting")
        try:
            inserted_stock_id = db.insert_record(
                collection="depot_stock_control", payload=stock
            )

            st.session_state["app_data"]["depot_stock_control"] = db.fetch_records(
                collection="depot_stock_control"
            )

            if inserted_stock_id:
                loading.empty()
                st.toast(f":green[Successfully added stock id - {inserted_stock_id}]")

        except Exception as e:
            loading.empty()
            st.toast(f":red[Failed adding stock - {str(e)}]")
