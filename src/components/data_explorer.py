import streamlit as st
import pandas as pd
from streamlit_extras.metric_cards import style_metric_cards
from streamlit_extras.dataframe_explorer import dataframe_explorer


import database.database as db


# Define the module
def data_explorer(record: str, collection: str, column_config: dict):
    # Fetch data records
    records = st.session_state["app_data"][record]

    style_metric_cards(box_shadow=False, border_left_color="#067528")

    if len(records) > 0:
        # Convert the records _id to string for comparison
        for rd in records:
            rd["_id"] = str(rd["_id"])

        # Create a DataFrame from the records
        records_df = pd.DataFrame(records)

        # Display Metrics
        if collection == "pcs":
            m_col1, m_col2, m_col3, m_col4 = st.columns(4)
            m_col1.metric(label="PURCHASING CLERKS", value=len(records_df))
            m_col2.metric(
                label="MALES", value=len(records_df[records_df["GENDER"] == "Male"])
            )
            m_col3.metric(
                label="FEMALES", value=len(records_df[records_df["GENDER"] == "Female"])
            )
            m_col4.metric(
                label="COOPERATIVE GROUPS",
                value=(records_df["COOPERATIVE GROUP"].nunique()),
            )
        elif collection == "farmers":
            f_col1, f_col2, f_col3, f_col4, f_col5 = st.columns(5)
            f_col1.metric(label="FARMERS", value=len(records_df))
            f_col2.metric(
                label="MALES", value=len(records_df[records_df["SEX (M/F)"] == "M"])
            )
            f_col3.metric(
                label="FEMALES", value=len(records_df[records_df["SEX (M/F)"] == "F"])
            )
            f_col4.metric(
                label="FARM SIZE",
                value=(pd.to_numeric(records_df["FARM SIZE"], errors="coerce").sum()),
            )
            f_col5.metric(
                label="COOPERATIVE GROUPS",
                value=(records_df["COOPERATIVE GROUP"].nunique()),
            )
        elif collection == "cooperative_groups":
            c_col1, c_col2, c_col3, c_col4, c_col5 = st.columns(5)
            c_col1.metric(label="COOPERATIVE GROUPS", value=len(records_df))
            c_col2.metric(label="REGIONS", value=(records_df["REGION"].nunique()))
            c_col3.metric(
                label="DISTRICTS",
                value=(records_df["DISTRICT"][records_df["DISTRICT"] != ""].nunique()),
            )
            c_col4.metric(
                label="COMMUNITIES",
                value=(
                    records_df["COMMUNITY"][records_df["COMMUNITY"] != ""].nunique()
                ),
            )
            c_col5.metric(label="PURCHASING CLERKS", value=(records_df["PC"].nunique()))

        elif collection == "depot_stock_control":
            d_col1, d_col2, d_col3, d_col4, d_col5, d_col6 = st.columns(6)
            d_col1.metric(label="PURCHASING CLERKS", value=(records_df["PC"].nunique()))
            d_col2.metric(
                label="PRI EVACUATION (BAG)",
                value=(records_df["PRI-EVAC: BAG"].sum()),
            )
            d_col3.metric(
                label="PRI EVACUATION (CUM)",
                value=(records_df["PRI-EVAC: CUMULATIVE"].sum()),
            )
            d_col4.metric(
                label="SEC EVACUATION (BAG)",
                value=(records_df["SEC-EVAC: BAG"].sum()),
            )
            d_col5.metric(
                label="SEC EVACUATION (CUM)",
                value=(records_df["SEC-EVAC: CUMULATIVE"].sum()),
            )
            d_col6.metric(label="BALANCE", value=(records_df["BALANCE"].sum()))

        elif collection == "input_requests":
            i_col1, i_col2, i_col3, i_col4, i_col5, i_col6 = st.columns(6)
            i_col1.metric(label="NUMBER OF FARMERS", value=(len(records_df)))
            i_col2.metric(
                label="COOPERATIVE GROUPS",
                value=(records_df["COOPERATIVE GROUP"].nunique()),
            )
            i_col3.metric(
                label="TOTAL INPUTS SUPPLIED",
                value=(records_df["QUANTITY"].sum()),
            )
            i_col4.metric(
                label="TOTAL COST",
                value=(records_df["TOTAL COST"].sum()),
            )
            i_col5.metric(
                label="TOTAL AMOUNT PAID",
                value=(records_df["AMOUNT PAID"].sum()),
            )
            i_col6.metric(
                label="BALANCE REMAINING",
                value=(records_df["BALANCE"].sum()),
            )

        # Display the Data
        if record == "input_requests":
            st.dataframe(
                records_df,
                use_container_width=True,
                hide_index=True,
                column_config=column_config,
            )
        else:
            filtered_df = dataframe_explorer(df=records_df)
            for col in filtered_df.columns:
                if "DATE" in col.upper():
                    filtered_df[col] = pd.to_datetime(filtered_df[col]).dt.date
            st.dataframe(
                filtered_df,
                use_container_width=True,
                hide_index=True,
                column_config=column_config,
            )
    else:
        st.markdown(
            "<h3 style='color: #dddddd; text-align: center; margin-top:3rem'>No Records to Display! Please add record at the entry side</h3>",
            unsafe_allow_html=True,
        )
