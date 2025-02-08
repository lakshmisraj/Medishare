from database import medical_history_collection

# Save medical history
def save_medical_history(user_id, condition, medications, notes):
    medical_history_collection.insert_one({
        "user_id": user_id,
        "condition": condition,
        "medications": medications,
        "notes": notes
    })

# Retrieve medical history for a user
def get_medical_history(user_id):
    return list(medical_history_collection.find({"user_id": user_id}, {"_id": 0}))