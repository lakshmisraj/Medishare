from fastapi.testclient import TestClient
import sys
import os

# Add the 'backend' directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../backend')))
from backend.app import app  # Adjust the import based on your project structure


# Create the test client
client = TestClient(app)

def test_chatbot_response():
    mock_user_id = "H6713741"
    mock_user_input = "Give me fitness advice"

    # Make a test API request
    response = client.get(f"/chat/{mock_user_id}/{mock_user_input}")

    # Check if the response status code is 200
    assert response.status_code == 200, f"Unexpected status code: {response.status_code}"

    # Print the response (for debugging)
    print(response.json())

    # Ensure the chatbot provides a response
    assert "response" in response.json(), "No chatbot response found"
    assert "fitness_data" in response.json(), "No fitness data returned"