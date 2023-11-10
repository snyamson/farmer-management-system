import streamlit as st

import database.database as db


def render_delete(selected_data, data: str, collection: str = None):
    if selected_data:
        st.divider()

        st.markdown(
            "<h3 style='text-align: center; color: red'>Delete Confirmation</h3>",
            unsafe_allow_html=True,
        )

        st.divider()

        with st.container():
            col1, col2 = st.columns([5, 2])
            with col1:
                st.markdown(
                    f"""
                    <h3> RECORD NAME:
                    {selected_data.get("NAME")
                    if selected_data.get("NAME") is not None
                    else selected_data.get("NAME OF FARMER")}
                    </h3>
                    """,
                    unsafe_allow_html=True,
                )
            with col2:
                delete_button = st.button(
                    label="Delete",
                    use_container_width=True,
                    key=selected_data.get("_id"),
                )

                if delete_button:
                    try:  # Update record
                        results = db.delete_record(
                            collection=collection,
                            id=str(selected_data.get("_id")),
                        )

                        if results.acknowledged:
                            # Update Records in session state
                            records = db.fetch_records(collection=collection)
                            st.session_state["app_data"][data] = records

                            st.toast(
                                f":green[Successfully Deleted - {selected_data.get('NAME') if selected_data.get('NAME') is not None else selected_data.get('NAME OF FARMER')}]"
                            )

                        else:
                            st.toast(":red[Delete was not successful]")

                    except Exception as e:
                        st.toast(f":red[Error deleting record] - {str(e)}")
