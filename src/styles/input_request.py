import streamlit as st


def button_style(state: str):
    if state == "show":
        st.markdown(
            """
                    <style>
                        button.st-emotion-cache-91ryd5.ef3psqc12  {
                            display: block
                        }
                    </style>
                    """,
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            """
                    <style>
                        button.st-emotion-cache-91ryd5.ef3psqc12  {
                            display: none
                        }
                    </style>
                    """,
            unsafe_allow_html=True,
        )


def progress_style():
    st.markdown(
        """
                    <style>
                        details.st-emotion-cache-1h9usn1.eqpbllx4 {
                            display: none
                        }
                    </style>
                    """,
        unsafe_allow_html=True,
    )
