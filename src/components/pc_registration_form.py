import streamlit as st
from datetime import date
import database.database as db


def pc_registration_form():
    coop_group_data = st.session_state["app_data"]["coop_group_data"]

    with st.form(key=f"PC Data Entry", clear_on_submit=True):
        st.subheader("Purchasing Clerk Registration Form", divider="green")

        with st.container():
            column1, column2, column3 = st.columns(3)

            with column1:
                pc_name = st.text_input(label="Name", help="Enter Name")
                pc_edu_level = st.selectbox(
                    label="Education Level",
                    help="Select Education Level",
                    options=["MSL", "JHS", "SSCE", "TERTIARY", "NFE"],
                    index=None,
                )
                pc_mode_of_id = st.selectbox(
                    label="Mode of Identification",
                    help="Select Mode of Identification",
                    options=["Voters ID", "Passport", "NHIS", "Ghana Card"],
                    index=None,
                )
                pc_date_registered = st.date_input(
                    label="Date of Registration",
                    help="Select Date of Registration/Joining",
                )

            with column2:
                pc_dob = st.date_input(
                    label="Date of Birth",
                    help="Select Date of Birth",
                    min_value=date(year=1940, month=1, day=1),
                )
                pc_age = st.text_input(
                    label="Age",
                    help="Enter the Age of PC",
                )
                pc_id_number = st.text_input(
                    label="ID Number",
                    help="Enter the ID Number of PC",
                )
                pc_community = st.text_input(
                    label="Community of Operation",
                    help="Enter Community of Operation",
                )

            with column3:
                pc_contact = st.text_input(label="Contact", help="Enter Contact")

                pc_gender = st.selectbox(
                    label="Gender",
                    options=["Male", "Female"],
                    index=None,
                )
                pc_location = st.text_input(label="Location", help="Enter Location")
                pc_cooperative = st.selectbox(
                    label="Cooperative Group",
                    help="PC Cooperative Group",
                    options=coop_group_data,
                    format_func=lambda coop: coop["NAME"],
                    index=None,
                )

        with st.container():
            st.subheader("Guarantor 1 Information")
            column4, column5, column6 = st.columns(3)

            with column4:
                g1_name = st.text_input(label="Name", help="Enter Name", key="g1_name")
                g1_edu_level = st.selectbox(
                    key="g1_edu_level",
                    label="Education Level",
                    help="Select Education Level",
                    options=["MSL", "JHS", "SSCE", "TERTIARY", "NFE"],
                    index=None,
                )

            with column5:
                g1_dob = st.date_input(
                    key="g1_dob",
                    label="Date of Birth",
                    help="Select Date of Birth",
                    min_value=date(year=1940, month=1, day=1),
                )
                g1_mode_of_id = st.selectbox(
                    key="g1_moi",
                    label="Mode of Identification",
                    help="Select Mode of Identification",
                    options=["Voters ID", "Passport", "NHIS", "Ghana Card"],
                    index=None,
                )

            with column6:
                g1_gender = st.selectbox(
                    index=None,
                    key="g1_gender",
                    label="Gender",
                    options=["Male", "Female"],
                )

                g1_id_number = st.text_input(
                    key="g1_id",
                    label="ID Number",
                    help="Enter the ID Number",
                )

        with st.container():
            st.subheader("Guarantor 2 Information")
            column7, column8, column9 = st.columns(3)

            with column7:
                g2_name = st.text_input(label="Name", help="Enter Name", key="g2_name")
                g2_edu_level = st.selectbox(
                    key="g2_edu_level",
                    label="Education Level",
                    help="Select Education Level",
                    options=["MSL", "JHS", "SSCE", "TERTIARY", "NFE"],
                    index=None,
                )

            with column8:
                g2_dob = st.date_input(
                    key="g2_dob",
                    label="Date of Birth",
                    help="Select Date of Birth",
                    min_value=date(year=1940, month=1, day=1),
                )
                g2_mode_of_id = st.selectbox(
                    key="g2_moi",
                    label="Mode of Identification",
                    help="Select Mode of Identification",
                    options=["Voters ID", "Passport", "NHIS", "Ghana Card"],
                    index=None,
                )

            with column9:
                g2_gender = st.selectbox(
                    key="g2_gender",
                    label="Gender",
                    options=["Male", "Female"],
                    index=None,
                )

                g2_id_number = st.text_input(
                    key="g2_id",
                    label="ID Number",
                    help="Enter the ID Number",
                )

        with st.container():
            st.subheader("Upload Passport Pictures")
            column10, column11, column12 = st.columns(3)

            with column10:
                pc_image = st.file_uploader(
                    "PC Passport Photo",
                    type=["jpg", "png", "jpeg"],
                    key="pc_image",
                )

            with column11:
                g1_image = st.file_uploader(
                    "G1 Passport Photo",
                    type=["jpg", "png", "jpeg"],
                    key="g1_image",
                )

            with column12:
                g2_image = st.file_uploader(
                    "G2 Passport Photo",
                    type=["jpg", "png", "jpeg"],
                    key="g2_image",
                )

        with st.container():
            st.subheader("Attach Signed Agreement")
            pc_signed_agreement = st.file_uploader(
                "Upload Signed Agreement", type=["docx", "pdf"], key="pc_agreement"
            )

        pc = {
            "NAME": pc_name,
            "GENDER": pc_gender,
            "DATE OF BIRTH": pc_dob.isoformat(),
            "AGE": pc_age,
            "EDUCATION LEVEL": pc_edu_level,
            "COMMUNITY": pc_community,
            "CONTACT": pc_contact,
            "MODE OF IDENTIFICATION": pc_mode_of_id,
            "ID NUMBER": pc_id_number,
            "LOCATION": pc_location,
            "DATE REGISTERED": pc_date_registered.isoformat(),
            "COOPERATIVE GROUP": pc_cooperative["NAME"]
            if pc_cooperative is not None
            else None,
            "GUARANTOR 1 NAME": g1_name,
            "GUARANTOR 1 DATE OF BIRTH": g1_dob.isoformat(),
            "GUARANTOR 1 EDU LEVEL": g1_edu_level,
            "GUARANTOR 1 GENDER": g1_gender,
            "GUARANTOR 1 MODE OF IDENTIFICATION": g1_mode_of_id,
            "GUARANTOR 1 ID NUMBER": g1_id_number,
            "GUARANTOR 2 NAME": g2_name,
            "GUARANTOR 2 DATE OF BIRTH": g2_dob.isoformat(),
            "GUARANTOR 2 EDU LEVEL": g2_edu_level,
            "GUARANTOR 2 GENDER": g2_gender,
            "GUARANTOR 2 MODE OF IDENTIFICATION": g2_mode_of_id,
            "GUARANTOR 2 ID NUMBER": g2_id_number,
            "PC IMAGE": None,
            "G1 IMAGE": None,
            "G2 IMAGE": None,
            "PC SIGNED AGREEMENT": None,
        }

        pc_submit_button = st.form_submit_button(
            label="Submit", use_container_width=True
        )

        if pc_submit_button:
            if pc_image or g1_image or g2_image or pc_signed_agreement is not None:
                with st.spinner(text="Uploading......"):
                    # Store the PC image in Cloudinary
                    pc_image_url = None
                    if pc_image:
                        pc_image_url = db.upload_file(file=pc_image, folder=pc_name)

                    # Store the Guarantor 1 image in Cloudinary
                    g1_image_url = None
                    if g1_image:
                        g1_image_url = db.upload_file(g1_image, folder=pc_name)

                    # Store the Guarantor 2 image in Cloudinary
                    g2_image_url = None
                    if g2_image:
                        g2_image_url = db.upload_file(g2_image, folder=pc_name)

                    # Store the PC signed agreement (PDF or DOCX) in Cloudinary
                    pc_signed_agreement_url = None
                    if pc_signed_agreement:
                        pc_signed_agreement_url = db.upload_file(
                            pc_signed_agreement, folder=pc_name
                        )

                    # Update the PC dictionary with URLS
                    pc["PC IMAGE"] = pc_image_url
                    pc["G1 IMAGE"] = g1_image_url
                    pc["G2 IMAGE"] = g2_image_url
                    pc["PC SIGNED AGREEMENT"] = pc_signed_agreement_url

                    # Save it to mongodb pcs collection
                    inserted_id = db.insert_record(collection="pcs", payload=pc)

                    # Refresh the pcs_name_id and pcs_data in the session state
                    pcs_name_id = db.fetch_names_and_ids(collection="pcs")
                    pcs_data = db.fetch_records(collection="pcs")
                    st.session_state["app_data"]["pcs_name_id"] = pcs_name_id
                    st.session_state["app_data"]["pcs_data"] = pcs_data

                    st.toast(f":green[Successfully added PC - {inserted_id}]")

            else:
                st.toast(":red[Please upload at least one image to submit the form.]")
