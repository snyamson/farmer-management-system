import streamlit as st
from datetime import datetime

import database.database as db


def depot_stock_update_form(stock_to_update: dict):
    # Perform Data Fetching
    pcs_data = st.session_state["app_data"]["pcs_data"]

    with st.form(key="Depot Stock Control Update Form", clear_on_submit=True):
        # Form Title
        st.subheader(
            f"Update Stock WayBill Number - {stock_to_update.get('WAYBILL NUMBER')}",
            divider="green",
        )

        col1, col2, col3 = st.columns(3)

        with col1:
            entry_date = st.date_input(
                label="Date",
                value=datetime.strptime(stock_to_update.get("DATE"), "%Y-%m-%d"),
                key="update_date",
            )

        with col2:
            waybill_number = st.text_input(
                label="WayBill Number",
                value=stock_to_update.get("WAYBILL NUMBER"),
                key="update_waybill",
            )

        with col3:
            society = st.text_input(
                label="Society",
                value=stock_to_update.get("SOCIETY"),
                key="update_society",
            )

        pc = st.selectbox(
            label="PC",
            options=pcs_data,
            format_func=lambda pc: pc["NAME"],
            index=next(
                (
                    index
                    for index, pc in enumerate(pcs_data)
                    if pc["NAME"] == stock_to_update.get("PC")
                ),
                None,
            ),
            key="update_pc",
        )

        with st.container():
            st.subheader("Primary Evacuation")
            col4, col5 = st.columns(2)

            with col4:
                pri_bag = st.number_input(
                    label="Bag",
                    min_value=0,
                    value=stock_to_update.get("PRI-EVAC: BAG"),
                    key="update_pri_bag",
                )

            with col5:
                pri_cumulative = st.number_input(
                    label="Cumulative",
                    min_value=0,
                    value=stock_to_update.get("PRI-EVAC: CUMULATIVE"),
                    key="update_pri_cum",
                )

        with st.container():
            st.subheader("Secondary Evacuation")
            col6, col7 = st.columns(2)

            with col6:
                sec_bag = st.number_input(
                    label="Bag",
                    min_value=0,
                    value=stock_to_update.get("SEC-EVAC: BAG"),
                    key="update_sec_bag",
                )

            with col7:
                sec_cumulative = st.number_input(
                    label="Cumulative",
                    min_value=0,
                    value=stock_to_update.get("SEC-EVAC: CUMULATIVE"),
                    key="update_sec_cum",
                )

        balance = st.number_input(
            label="Balance",
            min_value=0,
            value=stock_to_update.get("BALANCE"),
            key="update_balance",
        )

        submit_button = st.form_submit_button(
            label="Update Stock", use_container_width=True, type="primary"
        )

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
        loading = st.info("Updating..")
        try:
            results = db.update_record(
                collection="depot_stock_control",
                payload=stock,
                id=str(stock_to_update.get("_id")),
            )

            if results.acknowledged:
                # Update the data
                st.session_state["app_data"]["depot_stock_control"] = db.fetch_records(
                    collection="depot_stock_control"
                )
                # Remove the loader
                loading.empty()

                st.toast(
                    f":green[Successfully updated stock id - {stock_to_update.get('_id')}]"
                )

        except Exception as e:
            loading.empty()
            st.toast(f":red[Failed updating stock - {str(e)}]")
