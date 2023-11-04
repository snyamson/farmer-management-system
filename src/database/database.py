import streamlit as st
from pymongo import MongoClient
from dotenv import load_dotenv
from urllib.parse import quote_plus
from bson import ObjectId
import os

# Import the Cloudinary libraries
import cloudinary
import cloudinary.uploader
import cloudinary.api

# Load the .env file into the environment
load_dotenv()

# Access the environment variables
CLOUDINARY_CLOUD_NAME = os.getenv("CLOUDINARY_CLOUD_NAME")
CLOUDINARY_API_KEY = os.getenv("CLOUDINARY_API_KEY")
CLOUDINARY_API_SECRET = os.getenv("CLOUDINARY_API_SECRET")
DATABASE_USERNAME = os.getenv("DATABASE_USERNAME")
DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD")
DATABASE_CLUSTER_NAME = os.getenv("DATABASE_CLUSTER_NAME")
DATABASE_NAME = os.getenv("DATABASE_NAME")


# Global Configuration
cloudinary.config(
    cloud_name=CLOUDINARY_CLOUD_NAME,
    api_key=CLOUDINARY_API_KEY,
    api_secret=CLOUDINARY_API_SECRET,
    secure=True,
)


# Database Instance Configuration
# Determine if the code is running in production or locally
if os.getenv("ENVIRONMENT") == "production":
    # Code is running in production mode
    database_server = "remote"
else:
    # Code is running locally
    database_server = "local"


# Define the connection to remote server or local database
@st.cache_resource()
def init_db(server: str):
    client = None
    if server == "remote":
        uri = "mongodb+srv://%s:%s@%s" % (
            quote_plus(DATABASE_USERNAME),
            quote_plus(DATABASE_PASSWORD),
            DATABASE_CLUSTER_NAME,
        )

        # Create a new client and connect to the Remote server
        client = MongoClient(uri)
    else:
        # Create a new client and connect to the Local server
        client = MongoClient("localhost", 27017)

    # Send a ping to confirm a successful connection
    try:
        client.admin.command("ping")
        print("Successfully connected to the Database")
    except Exception as e:
        print("Error connecting to the database", e)

    db = client[DATABASE_NAME]


    return db

# Initialize Database and get db instance
db = init_db(server=database_server)


# Insert Record to the database
def insert_record(collection: str, payload: dict):
    data_collection = db[collection]
    try:
        # Insert the record and return it _id
        inserted_id = data_collection.insert_one(payload).inserted_id
        return inserted_id
    except Exception as e:
        print("Error Inserting Record", e)
        return None


# Fetch all records from the database
def fetch_records(collection: str):
    data_collection = db[collection]
    try:
        # Fetch all records and return it
        records = data_collection.find({})
        return list(records)
    except Exception as e:
        print("Error fetching all records", e)
        return None


# Update record in the database
def update_record(collection: str, id: str, payload: dict):
    data_collection = db[collection]
    try:
        # Perform the record update
        results = data_collection.update_one({"_id": ObjectId(id)}, {"$set": payload})
        return results
    except Exception as e:
        print("Error updating record", e)
        return None


# Fetch all record names and ids in a collection
def fetch_names_and_ids(collection: str):
    data_collection = db[collection]
    try:
        # Find all records in the collection -> Return the names and ids
        records = data_collection.find({})
        names_and_ids = [
            {"NAME": record["NAME"], "_id": str(record["_id"])} for record in records
        ]
        return names_and_ids
    except Exception as e:
        print("Error fetching records", e)
        return None


# Fetch record using id
def fetch_record_by_id(collection: str, id: str):
    data_collection = db[collection]
    try:
        # Find the record and return it
        record_id = ObjectId(id)
        found_record = data_collection.find_one({"_id": record_id})
        return found_record
    except Exception as e:
        print("Error fetching record", e)
        return None


# Upload the image to Cloudinary and Return the secure url
@st.cache_resource()
def upload_file(file, folder):
    try:
        result = cloudinary.uploader.upload(
            file,
            use_filename=True,
            unique_filename=False,
            overwrite=True,
            folder=folder,
            resource_type="auto",
        )
        return result["secure_url"]
    except Exception as e:
        print(f"Error uploading -- {file}", e)
        return None

# Load initial application data from the database
def load_initial_app_data():
    # Check if data is already loaded in session state
    if "app_data" not in st.session_state:
        # Load initial application data from the database
        coop_group_name_id = fetch_names_and_ids(collection="cooperative_groups")
        coop_group_data = fetch_records(collection="cooperative_groups")
        pcs_name_id = fetch_names_and_ids(collection="pcs")
        pcs_data = fetch_records(collection="pcs")
        farmers_data = fetch_records(collection="farmers")

        # Update session state with the new data
        st.session_state["app_data"] = {
            "coop_group_name_id": coop_group_name_id,
            "coop_group_data": coop_group_data,
            "pcs_name_id": pcs_name_id,
            "pcs_data": pcs_data,
            "farmers_data": farmers_data,
        }

    # Check for Authenticated Users
    if "authentication_status" not in st.session_state:
        st.session_state["authentication_status"] = None

    if "logout" not in st.session_state:
        st.session_state["logout"] = None

    if "name" not in st.session_state:
        st.session_state["name"] = None
 

# USER AUTHENTICATION MANAGEMENT

# Create user
def create_user(user:dict):
    users = db['users']
    try:
        user_id = users.insert_one(user)
        return user_id
    except Exception as e:
        print('Error Adding user', e)
