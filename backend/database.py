import certifi
from pymongo import MongoClient
import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Get MongoDB URI from .env file
MONGO_URI = os.getenv("MONGO_URI")

if not MONGO_URI:
    raise ValueError("MONGO_URI is not set in the .env file!")

# Connect to MongoDB
client = MongoClient(MONGO_URI, tlsCAFile=certifi.where())
db = client.medishare
users_collection = db.users

# Function to add a patient with new fields
def add_patient(name, email, mobile, dob, address, gender, govt_id, insurance_provider, insurance_number, emergency_contact):
    patient = {
        "name": name,
        "email": email,
        "mobile": mobile,
        "dob": dob,
        "address": address,
        "gender": gender,
        "govt_id": govt_id,
        "insurance_provider": insurance_provider,
        "insurance_number": insurance_number,
        "emergency_contact": emergency_contact
    }
    collection.insert_one(patient)

users_collection = db.users  # Users collection

# Function to get user by email
def get_user_by_email(email):
    return users_collection.find_one({"email": email})