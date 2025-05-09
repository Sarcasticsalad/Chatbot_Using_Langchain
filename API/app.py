from fastapi import FastAPI
from langchain.prompts import ChatPromptTemplate
from langchain.chat_models import ChatOpenAI
from langserve import add_routes
import uvicorn 
import os
from langchain_ollama.llms import OllamaLLM
from dotenv import load_dotenv

# loading the environment variables
load_dotenv()

# Creating FastAPI
app = FastAPI(
    title="Langchain Serves",
    version="1.0",
    description="A simple API server"
)

# Creating Routes
add_routes(
    app,
    path="/chatbot"
)

## Integrating prompt template

# Initializing model
model = OllamaLLM(model="qwen2.5-coder:latest")

# Creating a prompt
prompt = ChatPromptTemplate.from_template("Write an essay about {topic} with 100 words")

add_routes(
    app,
    prompt|model,
    path="/essay"
)


# Dunder Function
if __name__ == "__main__":
    uvicorn.run(app,host="localhost", port=8000)






