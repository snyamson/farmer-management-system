import streamlit as st

from components.authenticator import authenticator


# Define the Module
def app_bar(title:str, superuser:bool):
    if superuser:
        # Split the screen into two columns with a ratio of 5:2
        header_col_1, header_col_2 = st.columns([5, 2])

        # Create the first column for the title
        with header_col_1:
            # Display a styled h1 title using Markdown
            st.markdown(
                f"<h1 style='color: green; margin-bottom: 0rem'>{title}</h1>",
                unsafe_allow_html=True,
            )

        # Create the second column for additional content
        with header_col_2:
            # Insert a line break to add spacing
            st.markdown("<br>", unsafe_allow_html=True)
            col1, col2 = st.columns([1, 2])
            with col1:
                # Create a button for logout
                authenticator.logout("Logout")
            with col2:
                # Manage Users
                manage_users_button = st.button(label="Manage Users")
    else:
        # Split the screen into two columns with a ratio of 5:1
        header_col_1, header_col_2 = st.columns([5, 1])

        # Create the first column for the title
        with header_col_1:
            # Display a styled h1 title using Markdown
            st.markdown(
                f"<h1 style='color: green; margin-bottom: 0rem'>{title}</h1>",
                unsafe_allow_html=True,
            )

        # Create the second column for additional content
        with header_col_2:
            # Insert a line break to add spacing
            st.markdown("<br>", unsafe_allow_html=True)
            # Create a button for logout
            authenticator.logout("Logout")

    if superuser:         
        return manage_users_button