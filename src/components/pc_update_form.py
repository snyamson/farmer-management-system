import streamlit as st
from datetime import datetime
from datetime import date
import database.database as db


def pc_update_form(pc_to_update: dict):
    coop_group_name_id = st.session_state["app_data"]["coop_group_name_id"]

    # Define the Name Options for SelectBoxes
    coop_options = [coop["NAME"] for coop in coop_group_name_id]

    with st.form(key="PC Data Update", clear_on_submit=True):
        st.subheader(f"Update: {pc_to_update['NAME']}", divider="green")

        with st.container():
            column1, column2, column3 = st.columns(3)

            # Create Static Values
            edu_levels = ["MSL", "JHS", "SSCE", "TERTIARY", "NFE"]
            mode_of_id = [
                "Voters ID",
                "Passport",
                "NHIS",
                "Ghana Card",
            ]
            gender = ["Male", "Female"]

            with column1:
                pc_name = st.text_input(
                    label="Name",
                    help="Enter Name",
                    value=pc_to_update["NAME"],
                )
                pc_edu_level = st.selectbox(
                    label="Education Level",
                    help="Select Education Level",
                    options=edu_levels,
                    index=edu_levels.index(pc_to_update["EDUCATION LEVEL"])
                    if pc_to_update["EDUCATION LEVEL"] in edu_levels
                    else 0,
                )
                pc_mode_of_id = st.selectbox(
                    label="Mode of Identification",
                    help="Select Mode of Identification",
                    options=mode_of_id,
                    index=mode_of_id.index(pc_to_update["MODE OF IDENTIFICATION"])
                    if pc_to_update["MODE OF IDENTIFICATION"] in mode_of_id
                    else 0,
                )
                pc_date_registered = st.date_input(
                    label="Date of Registration",
                    help="Select Date of Registration/Joining",
                    value=datetime.strptime(
                        pc_to_update["DATE REGISTERED"], "%Y-%m-%d"
                    ),
                )

            with column2:
                pc_dob = st.date_input(
                    label="Date of Birth",
                    help="Select Date of Birth",
                    min_value=date(year=1940, month=1, day=1),
                    value=datetime.strptime(pc_to_update["DATE OF BIRTH"], "%Y-%m-%d"),
                )
                pc_age = st.text_input(
                    label="Age",
                    help="Enter the Age of PC",
                    value=pc_to_update["AGE"],
                )
                pc_id_number = st.text_input(
                    label="ID Number",
                    help="Enter the ID Number of PC",
                    value=pc_to_update["ID NUMBER"],
                )
                pc_community = st.text_input(
                    label="Enter Community of Operation",
                    help="Enter Community of Operation",
                    value=pc_to_update["COMMUNITY"],
                )

            with column3:
                pc_contact = st.text_input(
                    label="Enter Contact",
                    help="Enter Contact",
                    value=pc_to_update["CONTACT"],
                )
                pc_gender = st.selectbox(
                    label="Gender",
                    options=gender,
                    index=gender.index(pc_to_update["GENDER"])
                    if pc_to_update["GENDER"] in gender
                    else 0,
                )
                pc_location = st.text_input(
                    label="Enter Location",
                    help="Enter Location",
                    value=pc_to_update["LOCATION"],
                )
                pc_cooperative = st.selectbox(
                    label="Cooperative Group",
                    help="PC Cooperative Group",
                    options=coop_options,
                )

        with st.container():
            st.subheader("Guarantor 1 Information")
            column4, column5, column6 = st.columns(3)

            with column4:
                g1_name = st.text_input(
                    label="Name",
                    help="Enter Name",
                    key="g1u_name",
                    value=pc_to_update["GUARANTOR 1 NAME"],
                )
                g1_edu_level = st.selectbox(
                    key="g1u_edu_level",
                    label="Education Level",
                    help="Select Education Level",
                    options=edu_levels,
                    index=edu_levels.index(pc_to_update["GUARANTOR 1 EDU LEVEL"])
                    if pc_to_update["GUARANTOR 1 EDU LEVEL"] in edu_levels
                    else 0,
                )

            with column5:
                g1_dob = st.date_input(
                    key="g1u_dob",
                    label="Date of Birth",
                    help="Select Date of Birth",
                    min_value=date(year=1940, month=1, day=1),
                    value=datetime.strptime(
                        pc_to_update["GUARANTOR 1 DATE OF BIRTH"], "%Y-%m-%d"
                    ),
                )
                g1_mode_of_id = st.selectbox(
                    key="g1u_moi",
                    label="Mode of Identification",
                    help="Select Mode of Identification",
                    options=mode_of_id,
                    index=mode_of_id.index(
                        pc_to_update["GUARANTOR 1 MODE OF IDENTIFICATION"]
                    )
                    if pc_to_update["GUARANTOR 1 MODE OF IDENTIFICATION"] in mode_of_id
                    else 0,
                )

            with column6:
                g1_gender = st.selectbox(
                    key="g1u_gender",
                    label="Gender",
                    options=gender,
                    index=gender.index(pc_to_update["GUARANTOR 1 GENDER"])
                    if pc_to_update["GUARANTOR 1 GENDER"] in gender
                    else 0,
                )

                g1_id_number = st.text_input(
                    key="g1u_id",
                    label="ID Number",
                    help="Enter the ID Number",
                    value=pc_to_update["GUARANTOR 1 ID NUMBER"],
                )

        with st.container():
            st.subheader("Guarantor 2 Information")
            column7, column8, column9 = st.columns(3)

            with column7:
                g2_name = st.text_input(
                    label="Name",
                    help="Enter Name",
                    key="g2u_name",
                    value=pc_to_update["GUARANTOR 2 NAME"],
                )
                g2_edu_level = st.selectbox(
                    key="g2u_edu_level",
                    label="Education Level",
                    help="Select Education Level",
                    options=edu_levels,
                    index=edu_levels.index(pc_to_update["GUARANTOR 2 EDU LEVEL"])
                    if pc_to_update["GUARANTOR 2 EDU LEVEL"] in edu_levels
                    else 0,
                )

            with column8:
                g2_dob = st.date_input(
                    key="g2u_dob",
                    label="Date of Birth",
                    help="Select Date of Birth",
                    min_value=date(year=1940, month=1, day=1),
                    value=datetime.strptime(
                        pc_to_update["GUARANTOR 2 DATE OF BIRTH"], "%Y-%m-%d"
                    ),
                )
                g2_mode_of_id = st.selectbox(
                    key="g2u_moi",
                    label="Mode of Identification",
                    help="Select Mode of Identification",
                    options=mode_of_id,
                    index=mode_of_id.index(
                        pc_to_update["GUARANTOR 2 MODE OF IDENTIFICATION"]
                    )
                    if pc_to_update["GUARANTOR 2 MODE OF IDENTIFICATION"] in mode_of_id
                    else 0,
                )

            with column9:
                g2_gender = st.selectbox(
                    key="g2u_gender",
                    label="Gender",
                    options=gender,
                    index=gender.index(pc_to_update["GUARANTOR 2 GENDER"])
                    if pc_to_update["GUARANTOR 2 GENDER"] in gender
                    else 0,
                )

                g2_id_number = st.text_input(
                    key="g2u_id",
                    label="ID Number",
                    help="Enter the ID Number",
                    value=pc_to_update["GUARANTOR 2 ID NUMBER"],
                )

        with st.container():
            st.subheader(":red[Upload New Passport Pictures to Update]")
            column10, column11, column12 = st.columns(3)

            with column10:
                pc_image = st.file_uploader(
                    "PC Passport Photo",
                    type=["jpg", "png", "jpeg"],
                    key="pcu_image",
                )

            with column11:
                g1_image = st.file_uploader(
                    "G1 Passport Photo",
                    type=["jpg", "png", "jpeg"],
                    key="g1u_image",
                )

            with column12:
                g2_image = st.file_uploader(
                    "G2 Passport Photo",
                    type=["jpg", "png", "jpeg"],
                    key="g2u_image",
                )

        with st.container():
            st.subheader(":red[Attach New Signed Agreement to Update]")
            pc_signed_agreement = st.file_uploader(
                "Upload Signed Agreement",
                type=["docx", "pdf"],
                key="pcu_agreement",
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
            "COOPERATIVE GROUP": pc_cooperative,
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

        pc_update_button = st.form_submit_button(
            label="Update Purchasing Clerk", use_container_width=True, type="primary"
        )

        if pc_update_button:           
                with st.spinner(text="Uploading......"):
                    # Store the PC image in Cloudinary
                    pc_image_url = pc_to_update["PC IMAGE"]
                    if pc_image:
                        pc_image_url = db.upload_file(file=pc_image, folder=pc_name)

                    # Store the Guarantor 1 image in Cloudinary
                    g1_image_url = pc_to_update["G1 IMAGE"]
                    if g1_image:
                        g1_image_url = db.upload_file(g1_image, folder=pc_name)

                    # Store the Guarantor 2 image in Cloudinary
                    g2_image_url = pc_to_update["G2 IMAGE"]
                    if g2_image:
                        g2_image_url = db.upload_file(g2_image, folder=pc_name)

                    # Store the PC signed agreement (PDF or DOCX) in Cloudinary
                    pc_signed_agreement_url = pc_to_update["PC SIGNED AGREEMENT"]
                    if pc_signed_agreement:
                        pc_signed_agreement_url = db.upload_file(
                            pc_signed_agreement, folder=pc_name
                        )

                    # Update the PC dictionary with URLS
                    pc["PC IMAGE"] = pc_image_url
                    pc["G1 IMAGE"] = g1_image_url
                    pc["G2 IMAGE"] = g2_image_url
                    pc["PC SIGNED AGREEMENT"] = pc_signed_agreement_url
                
                    # Update date in pcs collection
                    results = db.update_record(collection="pcs", payload=pc, id=pc_to_update.get("_id"))

                    if results.acknowledged:

                        # Refresh the pcs_name_id and pcs_data in the session state
                        pcs_name_id = db.fetch_names_and_ids(
                                    collection="pcs"
                                )
                        pcs_data = db.fetch_records(
                                    collection="pcs"
                                )
                        st.session_state["app_data"]['pcs_name_id'] = pcs_name_id
                        st.session_state["app_data"]['pcs_data'] = pcs_data

                        st.toast(f":green[Successfully updated PC - {pc_to_update['_id']}]")
                    
                    else:
                        st.toast(":red[Update was not successful]")

