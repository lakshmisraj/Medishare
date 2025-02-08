from fastapi import APIRouter, HTTPException
from database import profiles_collection

router = APIRouter(prefix="/profiles", tags=["Profiles"])

@router.get("/{user_id}")
def get_user_profiles(user_id: str):
    # Fetch profiles for the specific user
    profiles = list(profiles_collection.find({"user_id": user_id}, {"_id": 0}))  # Exclude _id
    if not profiles:
        raise HTTPException(status_code=404, detail="No profiles found for this user.")
    return {"profiles": profiles}