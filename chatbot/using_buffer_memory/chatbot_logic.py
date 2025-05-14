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

# === Load environment variables from .env ===
load_dotenv()

# Langsmith Tracing Setup if using LangSmith tracing/debugging
os.environ['LANGSMITH_TRACING'] = "false"
os.environ['LANGSMITH_API_KEY'] = os.getenv("LANGSMITH_API_KEY")
os.environ['LANGSMITH_ENDPOINT'] = os.getenv("LANGSMITH_ENDPOINT", "https://api.smith.langchain.com")
os.environ["LANGSMITH_PROJECT"] = os.getenv("LANGSMITH_PROJECT")

# === Defining Prompt Template with message placeholders ===
# Sets the structure of messages sent to the model 
prompt = ChatPromptTemplate([
        # Role: Sets assistant behavior
        SystemMessagePromptTemplate.from_template(
            "You are a helpful assistant. Please respond to the user queries"
        ),

        # Role: Adds conversation history (for memory)
        MessagesPlaceholder(variable_name="chat_history"),
        
        # Role: Adds the latest user question
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

# === Memory Handler ===
# Uses session_id to keep track of individual conversations
def get_memory(session_id: str):
    """
    Retrieves or initializes memory for a specific session_id.

    Args:
        session_id (str): Unique identifier for the conversation session.

    Returns:
        chat_memory (list): List of chat messages from the conversation.
    """

    # Initialize memory store if not yet created
    if "memory" not in st.session_state:
        st.session_state.memory = {}

    # If memory doesn't exist for this session, create it
    if session_id not in st.session_state.memory:
        st.session_state.memory[session_id] = ConversationBufferMemory(
            # Must match MessagesPlaceholder in the prompt
            memory_key="chat_history", 
            # Ensures chat messages are returned in proper format
            return_messages=True
        )    
    
    # Return only the chat memory (not the memory object) for use in RunnableWithMessageHistory
    return st.session_state.memory[session_id].chat_memory


# === LangChain Chain with Memory Support ===
# This chain handles prompting, generation, output parsing, and memory

# 1. Format input using the prompt
# 2. Generate response using the model
# 3. Parse output to string
# 4. Wrap final output in a dictionary

chain = prompt | llm | output_parser | RunnableLambda(lambda x: {"output": x})

# === Final Runnable with Memory Support ===

chat_chain = RunnableWithMessageHistory(
        # The full chain from prompt to parsed output
        runnable=chain,
        # Memory retriever
        get_session_history=get_memory,
        # Key from input dict to use as current user input
        input_messages_key="question",
        # Key used in prompt for history injection
        history_messages_key="chat_history",
        
)
