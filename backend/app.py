from fastapi import FastAPI
from database import profiles_collection

app = FastAPI()

@app.get("/profiles/")
def get_profiles():
    # Fetch all profiles from MongoDB
    profiles = list(profiles_collection.find({}, {"_id": 0}))  # Exclude MongoDB's _id
    return {"profiles": profiles}