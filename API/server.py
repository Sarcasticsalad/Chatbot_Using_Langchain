import sys
import os

# === Add the root directory to Python path ===
# This allows Python to find the chatbot module regardless of where the script is run from
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from langserve import add_routes
import uvicorn 
from chatbot.using_buffer_memory.chatbot_logic import chat_chain

# === Initialize FastAPI app ===
app = FastAPI(
    title="LangServe for Chatbot",
    version="1.0",
    description="A simple API server"
)

# === CORS Middleware ===
# This allows the frontend (e.g., Streamlit running on a different port) to access the backend
app.add_middleware(
    CORSMiddleware,
    # Allow requests from any origin (for development)
    allow_origins=["*"],
    # Allow cookies and credentials to be sent
    allow_credentials=True,
    # Allow all HTTP methods (GET, POST, etc.)
    allow_methods=["*"],
    # Allow all request headers
    allow_headers=["*"],

)

# Route for testing
@app.get("/ping")
def test_chat():
    return {"message": "API working"}


# === LangServe Chain Routing ===
# Adds the /chat endpoint which exposes the LangChain Runnable
# This allows POST requests to /chat/invoke with {"input": {"question": "..."}, "config": {...}}
# Example request body:
# {
#   "input": {"question": "What is LangChain?"},
#   "config": {
#       "configurable": {"session_id": "user-session"}
#   }
# }

add_routes(
    app,
    # The RunnableWithMessageHistory chain from your logic
    runnable=chat_chain,
    # Accessible at /chat/invoke
    path="/chat",
    
)

# === Start the server with Uvicorn ===
# Only runs when executed directly (not on import)
if __name__ == "__main__":
    uvicorn.run("API.server:app",host="localhost", port=8000)





