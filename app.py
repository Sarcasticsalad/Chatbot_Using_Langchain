from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_ollama.llms import OllamaLLM
import streamlit as st
import os
from dotenv import load_dotenv

load_dotenv()

# Langsmith Tracking
os.environ["LANGCHAIN_TRACKING_V2"] = "true"
os.environ["LANGCHAIN_API_KEY"] = os.getenv("LANGCHAIN_API_KEY")

## Defining Prompt Template
prompt=ChatPromptTemplate.from_messages(
    [
        ("system", "You are a helpful assistant. Please respond to the user queries",),
        ("user", "Question:{question}")
    ]
)

## Streamlit framework
st.title('Langchain Demo Chatbot')
input_text = st.text_input("Search for any topics you want...") 


#LLM
llm = OllamaLLM(model="qwen2.5-coder:3b")

# String output parser 
output_parser = StrOutputParser()

# Chain
chain = prompt|llm|output_parser

if input_text:
    st.write(chain.invoke({'question':input_text}))