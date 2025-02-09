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

@app.get("/fitness/{user_id}")
def get_latest_user_fitness(user_id: str):
    # Fetch the latest fitness record for the specific user
    latest_fitness = fitness_collection.find_one(
        {"user_id": user_id}, 
        {"_id": 0}, 
        sort=[("date", -1)]  # Sort by date descending to get the latest entry
    )
    
    if not latest_fitness:
        raise HTTPException(status_code=404, detail="No fitness record found for this user.")
    
    return {"fitness": latest_fitness}


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
        "inputs": user_input,
        "parameters": {
            "max_new_tokens": 150,  # Ensures the model generates new text
            "temperature": 0.7,  # Adjusts randomness in responses
            "top_p": 0.9  # Helps with diversity in responses
        }
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
    
def format_fitness_data(fitness_data):
    """Formats fitness data into a readable string."""
    if not fitness_data or "fitness" not in fitness_data:
        return "No recent fitness data available."
    data = fitness_data["fitness"]
    return (f"On {data['date']}, the user did {data['activity']} for {data['duration_hours']} hours, "
            f"burning {data['calories_burned']} calories. They walked {data['steps']} steps and slept for "
            f"{data['sleep_hours']} hours.")

# API Endpoint: Chatbot with Fitness Advice
@app.get("/chat/{user_id}/{user_input}")
def chat(user_id: str, user_input: str):
    try:
        # Fetch fitness data
        fitness_data = get_latest_user_fitness(user_id)
        fitness_summary = format_fitness_data(fitness_data)
        
        # Format user message with fitness info
        #fitness_summary = f"User activity: {fitness_data['activity']}, Calories burned: {fitness_data['calories_burned']}, Steps: {fitness_data['steps']}."
        combined_input = f"{user_input}. Based on the user's fitness history: {fitness_summary} What advice can you give?"
        
        print(f"Combined Input: {combined_input}")
        # Get chatbot response
        chatbot_response = get_huggingface_response(combined_input)

        return {"response": chatbot_response, "fitness_data": fitness_data}
    
    except HTTPException as e:
        raise e
    except Exception as e:
        print(f"Unexpected error: {e}")
        raise HTTPException(status_code=500, detail="An unexpected error occurred.")