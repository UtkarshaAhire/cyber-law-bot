import requests
import google.generativeai as genai

# Configure the Gemini API with the API key
genai.configure(api_key="AIzaSyBvr-VFrJY8KkTHWB7S2PVr4UNA0Z7ksqQ")

def test_chat():
    # The endpoint where your Flask chatbot is running
    url = "http://127.0.0.1:8000/chat"
    data = {
        "message": "What are the basic cyber laws?",
        "conversation_id": None
    }
    
    # Make a POST request to the chatbot
    response = requests.post(url, json=data)
    
    # Print the response from the chatbot
    print("Status Code:", response.status_code)
    print("Response:", response.json())

# Run the test
test_chat()
