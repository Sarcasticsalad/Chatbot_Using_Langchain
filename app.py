from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_ollama.llms import OllamaLLM
import streamlit as st
import os
from dotenv import load_dotenv

# Load the environment variables
load_dotenv()


# Langsmith Tracing Setup
os.environ['LANGSMITH_TRACING'] = "true"
os.environ['LANGSMITH_API_KEY'] = os.getenv("LANGSMITH_API_KEY")
os.environ['LANGSMITH_ENDPOINT'] = os.getenv("LANGSMITH_ENDPOINT")
os.environ["LANGCHAIN_PROJECT"] = os.getenv("LANGCHAIN_PROJECT")


# Defining Prompt Template
prompt=ChatPromptTemplate.from_messages(
    [
        ("system", "You are a helpful assistant. Please respond to the user queries",),
        ("user", "Question:{question}")
    ]
)

# Streamlit framework
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