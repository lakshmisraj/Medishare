from fastapi import APIRouter, Depends, HTTPException
from fastapi_jwt_auth import AuthJWT
from database import profiles_collection

# Create FastAPI Router
router = APIRouter(prefix="/profile", tags=["Profile"])

@router.get("/")
def get_profile(Authorize: AuthJWT = Depends()):
    try:
        # Ensure the request includes a valid JWT token
        Authorize.jwt_required()

        # Get the user ID from the JWT token
        user_id = Authorize.get_jwt_subject()
        print(f"✅ User ID from JWT: {user_id}")  # Debug log

        # Retrieve profile from MongoDB
        profile = profiles_collection.find_one({"user_id": str(user_id)}, {"_id": 0})
        
        if not profile:
            print("❌ Profile not found in MongoDB!")  # Debug log
            raise HTTPException(status_code=404, detail="Profile not found")

        print(f"✅ Profile Data Retrieved: {profile}")  # Debug log
        return profile

    except Exception as e:
        print(f"❌ Error in /profile/: {e}")  # Print error details
        raise HTTPException(status_code=500, detail="Internal Server Error")