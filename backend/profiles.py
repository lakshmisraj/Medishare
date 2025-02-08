from database import profiles_collection

# Save or update a user profile
def save_profile(user_id, profile_data):
    profiles_collection.update_one(
        {"user_id": user_id},
        {"$set": profile_data},
        upsert=True
    )

# Retrieve a user profile
def get_profile(user_id):
    return profiles_collection.find_one({"user_id": user_id}, {"_id": 0})