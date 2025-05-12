# == Imports ==
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_ollama.chat_models import ChatOllama
from langchain.memory import ConversationBufferMemory
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder, SystemMessagePromptTemplate, HumanMessagePromptTemplate
from langchain_core.runnables import RunnableWithMessageHistory, RunnableLambda

import streamlit as st
import os
from dotenv import load_dotenv

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "../../.env"))

# === Load environment variables ===
load_dotenv()

# Langsmith Tracing Setup
os.environ['LANGSMITH_TRACING'] = "false"
os.environ['LANGSMITH_API_KEY'] = os.getenv("LANGSMITH_API_KEY")
os.environ['LANGSMITH_ENDPOINT'] = os.getenv("LANGSMITH_ENDPOINT", "https://api.smith.langchain.com")
os.environ["LANGSMITH_PROJECT"] = os.getenv("LANGSMITH_PROJECT")

# === Defining Prompt Template with message placeholders ===
prompt = ChatPromptTemplate([
        # System message that instructs the assistant on behavior
        SystemMessagePromptTemplate.from_template(
            "You are a helpful assistant. Please respond to the user queries"
        ),

        # Chat history placeholder (required for memory)
        MessagesPlaceholder(variable_name="chat_history"),
        # User input (question)
        HumanMessagePromptTemplate.from_template("{question}")
        
    ]
)

# === Load the Chat Model ===
# ChatOllama can be replaced with OpenAI, Anthropic, etc.
# Note: Different models may require different memory or input formatting
llm = ChatOllama(model="qwen2.5-coder:latest")

# === String Output Parser === 
# Converts the structured output into a plain string for display
output_parser = StrOutputParser()

# === Memory Initialization Function ===
# Uses session_id to keep track of individual conversations
def get_memory(session_id: str):
    """
    Returns the conversation memory for the given session_id.
    Initializes a new ConversationBufferMemory if not already present.
    """
    if "memory" not in st.session_state:
        st.session_state.memory = {}

    if session_id not in st.session_state.memory:
        st.session_state.memory[session_id] = ConversationBufferMemory(
            # Must match the placeholder
            memory_key="chat_history", 
            # Required for proper memory replay
            return_messages=True
        )    
    
    # Only returning the chat_memory for use with RunnableWithMessageHistory
    return st.session_state.memory[session_id].chat_memory


# === Chain Setup with Memory Support ===
# RunnableWithMessageHistory is used to support persistent conversation state
chain = prompt | llm | output_parser | RunnableLambda(lambda x: {"output": x})
chat_chain = RunnableWithMessageHistory(
        runnable=chain,
        get_session_history=get_memory,
        input_messages_key="question",
        history_messages_key="chat_history",
        
)
