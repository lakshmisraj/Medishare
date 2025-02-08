from pymongo import MongoClient
import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Get MongoDB URI from .env file
MONGO_URI = os.getenv("MONGO_URI")

if not MONGO_URI:
    raise ValueError("⚠️ MONGO_URI is not set in the .env file!")

# Connect to MongoDB
client = MongoClient(MONGO_URI)
db = client.medishare  # Database
collection = db.records  # Collection