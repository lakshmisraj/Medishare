from fastapi import FastAPI, HTTPException
from database import profiles_collection, fitness_collection, vaccines_collection, medical_conditions_collection, family_medical_history_collection

app = FastAPI()

@app.get("/profiles/{user_id}")
def get_user_profiles(user_id: str):
    # Fetch profiles for the specific user
    profiles = list(profiles_collection.find({"user_id": user_id}, {"_id": 0}))  # Exclude _id
    if not profiles:
        raise HTTPException(status_code=404, detail="No profiles found for this user.")
    return {"profiles": profiles}

@app.get("/fitness/{user_id}")
def get_user_fitness(user_id: str):
    # Fetch profiles for the specific user
    fitness = list(fitness_collection.find({"user_id": user_id}, {"_id": 0}))  # Exclude _id
    if not fitness:
        raise HTTPException(status_code=404, detail="No fitness profiles found for this user.")
    return {"fitness": fitness}

@app.get("/vaccines/{user_id}")
def get_user_vaccines(user_id: str):
    # Fetch profiles for the specific user
    vaccines = list(vaccines_collection.find({"user_id": user_id}, {"_id": 0}))  # Exclude _id
    if not vaccines:
        raise HTTPException(status_code=404, detail="No vaccines found for this user.")
    return {"vaccines": vaccines}

# Get User Medical Conditions
@app.get("/medical_conditions/{user_id}")
def get_user_medical_conditions(user_id: str):
    medical_conditions = list(medical_conditions_collection.find({"user_id": user_id}, {"_id": 0}))
    if not medical_conditions:
        raise HTTPException(status_code=404, detail="No medical conditions found for this user.")
    return {"medical_conditions": medical_conditions}

# Get User Family Medical History
@app.get("/family_medical_history/{user_id}")
def get_user_family_medical_history(user_id: str):
    family_medical_history = list(family_medical_history_collection.find({"user_id": user_id}, {"_id": 0}))
    if not family_medical_history:
        raise HTTPException(status_code=404, detail="No family medical history found for this user.")
    return {"family_medical_history": family_medical_history}