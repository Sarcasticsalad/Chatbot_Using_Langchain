# == Imports ==
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_ollama.chat_models import ChatOllama
from langchain.memory import ConversationBufferMemory
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder, SystemMessagePromptTemplate, HumanMessagePromptTemplate
from langchain_core.runnables import RunnableWithMessageHistory

import streamlit as st
import os
from dotenv import load_dotenv

# === Load environment variables ===
load_dotenv()

# Langsmith Tracing Setup
os.environ['LANGSMITH_TRACING'] = "true"
os.environ['LANGSMITH_API_KEY'] = os.getenv("LANGSMITH_API_KEY")
os.environ['LANGSMITH_ENDPOINT'] = os.getenv("LANGSMITH_ENDPOINT")
os.environ["LANGCHAIN_PROJECT"] = os.getenv("LANGCHAIN_PROJECT")

# === Streamlit Framework Setup ===
st.title('Langchain Demo Chatbot')
input_text = st.text_input("Search for any topics you want...") 


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
chain = prompt | llm | output_parser
chat_chain = RunnableWithMessageHistory(
        runnable=chain,
        get_session_history=get_memory,
        input_messages_key="question",
        history_messages_key="chat_history",
        
)

# === Handling User Input ===
if input_text:

    session_id = 'user-session'

    response = chat_chain.invoke(
        {"question": input_text}, 
        config={"configurable":{"session_id":session_id}}
        )

    st.write(response)

# === Display Conversation History ===
# This shows the previous chat messages from the session
with st.expander("Conversation History"):
    memory = get_memory("user-session")

    for msg in memory.messages:
        # e.g., AIMessage -> AI
        role = type(msg).__name__.replace("Message", "")
        st.write(f"{role}:{msg.content}")    