import streamlit as st
import pandas as pd

import database.database as db


# Define the module
def data_explorer(record: str, collection:str, column_config: dict):
        # Fetch data records
        records = st.session_state['app_data'][record]

        # Convert the records _id to string for comparison
        for rd in records:
            rd["_id"] = str(rd["_id"])

        # Create a DataFrame from the records
        records_df = pd.DataFrame(records)

        # Display Metrics
        if collection == 'pcs':
            m_col1, m_col2, m_col3, m_col4 = st.columns(4)
            m_col1.metric(label='PURCHASING CLERKS', value=len(records_df))
            m_col2.metric(label='MALES', value=len(records_df[records_df['GENDER']=="Male"]))
            m_col3.metric(label='FEMALES', value=len(records_df[records_df['GENDER']=="Female"]))
            m_col4.metric(label='COOPERATIVE GROUPS', value=(records_df['COOPERATIVE GROUP'].nunique()))
        elif collection == 'farmers':
            f_col1, f_col2, f_col3, f_col4, f_col5 = st.columns(5)
            f_col1.metric(label='FARMERS', value=len(records_df))
            f_col2.metric(label='MALES', value=len(records_df[records_df['SEX (M/F)']=="M"]))
            f_col3.metric(label='FEMALES', value=len(records_df[records_df['SEX (M/F)']=="F"]))
            f_col4.metric(label='FARM SIZE', value=(pd.to_numeric(records_df['FARM SIZE'], errors='coerce').sum()))
            f_col5.metric(label='COOPERATIVE GROUPS', value=(records_df['COOPERATIVE GROUP'].nunique()))
        elif collection == 'cooperative_groups':
            c_col1, c_col2, c_col3, c_col4, c_col5 = st.columns(5)
            c_col1.metric(label='COOPERATIVE GROUPS', value=len(records_df))
            c_col2.metric(label='REGIONS', value=(records_df['REGION'].nunique()))
            c_col3.metric(label='DISTRICTS', value=(records_df['DISTRICT'][records_df['DISTRICT'] != ''].nunique()))
            c_col4.metric(label='COMMUNITIES', value=(records_df['COMMUNITY'][records_df['COMMUNITY'] != ''].nunique()))
            c_col5.metric(label='PURCHASING CLERKS', value=(records_df['PC'].nunique()))

        # Display the Ag-Grid
        edited_records_grid = st.data_editor(
            records_df,
            use_container_width=True,
            hide_index=True,
            column_config=column_config,
        )

        # Initialize an empty dictionary to store edited fields
        edited_fields_dict = {}

        # Iterate through each column (field) in the data
        for field in edited_records_grid.columns:
            edited_rows = (edited_records_grid[field] != records_df[field])
            edited_rows = edited_rows.fillna(False)  # Replace NaN with False
            
            for idx, has_changed in enumerate(edited_rows):
                if has_changed:
                    record_id = edited_records_grid.at[idx, "_id"]
                    field_value = edited_records_grid.at[idx, field]
                    if record_id not in edited_fields_dict:
                        edited_fields_dict[record_id] = []
                    edited_fields_dict[record_id].append((field, field_value))

        # Save the Edited DataFrame to Database
        save_changes_btn = None

        if len(edited_fields_dict.items()) > 0:
            save_changes_btn = st.button(
                label="Save Changes to Database",
                use_container_width=True,
                type="primary",
                key=record,
            )

        if save_changes_btn:
            try:
                for record_id, edited_fields in edited_fields_dict.items():
                    # Create an update dictionary with the edited fields
                    update_dict = {}
                    for field, value in edited_fields:
                        update_dict[field] = value

                    # Update the document in the MongoDB collection
                    db.update_record(collection, record_id, update_dict)

                    # Update farmers_data in session state
                    st.session_state['app_data'][record] = db.fetch_records(
                        collection=collection
                    )

                st.toast(":green[Successfully Updated Edited Fields]")

            except Exception as e:
                st.toast(f":red[Error Updating Edited Fields - {str(e)}]")