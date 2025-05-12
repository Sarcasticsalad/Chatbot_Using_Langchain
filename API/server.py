import sys
import os

# Add the project root directory to sys.path so Python can find the chatbot folder
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from fastapi import FastAPI
from fastapi.responses import PlainTextResponse
from langserve import add_routes
import uvicorn 
from chatbot.using_buffer_memory.chatbot_logic import chat_chain
from dotenv import load_dotenv

# loading the environment variables
load_dotenv()

# Creating FastAPI
app = FastAPI(
    title="LangServe for Chatbot",
    version="1.0",
    description="A simple API server"
)

# Route for testing
@app.get("/ping")
def test_chat():
    return {"message": "API working"}



# Adding routes 
add_routes(
    app,
    runnable=chat_chain,
    path="/chat",
    
)

#  Run the server
if __name__ == "__main__":
    uvicorn.run("API.server:app",host="localhost", port=8000)





