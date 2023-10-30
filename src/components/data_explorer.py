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