from fastapi import FastAPI, HTTPException
from database import profiles_collection, fitness_collection, vaccines_collection, medical_conditions_collection, family_medical_history_collection
import requests
import os

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


# Hugging Face API setup
HUGGINGFACE_API_URL = "https://api-inference.huggingface.co/models/microsoft/DialoGPT-medium"  # Replace with your Hugging Face model URL
HUGGINGFACE_API_TOKEN = os.getenv("HUGGINGFACE_API_TOKEN")#"HUGGINGFACE_API_TOKEN"  # Replace with your Hugging Face token

# Function to get the response from Hugging Face API
def get_huggingface_response(user_input: str):
    headers = {
        "Authorization": f"Bearer {HUGGINGFACE_API_TOKEN}"
    }

    # Prepare the data payload for Hugging Face API
    data = {
        "inputs": user_input
    }
    try:
    # Make the request to Hugging Face API
        response = requests.post(HUGGINGFACE_API_URL, headers=headers, json=data)

        print(f"Response Status Code: {response.status_code}")
        print(f"Response Content: {response.text}")

        if response.status_code != 200:
            raise HTTPException(status_code=500, detail="Error while fetching response from Hugging Face API")

        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Request Exception: {e}")
        raise HTTPException(status_code=500, detail=f"Error in Hugging Face API request: {e}")

# FastAPI endpoint to interact with the Hugging Face API
@app.get("/chat/{user_input}")
def chat(user_input: str):
    try:
        # Get response from Hugging Face
        chatbot_response = get_huggingface_response(user_input)
        return {"response": chatbot_response}
    except HTTPException as e:
        raise e
    except Exception as e:
        print(f"Unexpected error: {e}")  # Log the error
        raise HTTPException(status_code=500, detail="An unexpected error occurred.")