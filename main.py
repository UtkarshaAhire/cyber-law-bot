from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import google.generativeai as genai
from typing import Optional
import os
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv  # Import dotenv to load environment variables

# Load environment variables from .env
load_dotenv()

# Initialize FastAPI app
app = FastAPI(
    title="Legal Chatbot API",
    description="API service for cyber law chatbot using Gemini",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Modify this in production to specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models for request/response
class ChatRequest(BaseModel):
    message: str
    conversation_id: Optional[str] = None

class ChatResponse(BaseModel):
    response: str
    conversation_id: str

# Initialize Gemini using environment variable
def initialize_gemini():
    try:
        # Get the API key from the environment variable
        gemini_api_key = os.getenv('AIzaSyBvr-VFrJY8KkTHWB7S2PVr4UNA0Z7ksqQ')
        
        if not gemini_api_key:
            raise ValueError("GEMINI_API_KEY is not set in environment variables!")
        
        genai.configure(api_key=gemini_api_key)
        model = genai.GenerativeModel('gemini-pro')
        return model
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to initialize Gemini: {str(e)}")

# Store conversations (in production, use a proper database)
conversations = {}

@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    try:
        model = initialize_gemini()
        
        # Get or create conversation history
        if request.conversation_id and request.conversation_id in conversations:
            chat = conversations[request.conversation_id]
        else:
            chat = model.start_chat(history=[])
            request.conversation_id = str(len(conversations))
            conversations[request.conversation_id] = chat
        
        # Generate response
        response = chat.send_message(request.message)
        
        return ChatResponse(
            response=response.text,
            conversation_id=request.conversation_id
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    return {"status": "healthy"}
