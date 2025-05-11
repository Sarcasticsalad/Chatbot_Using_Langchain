from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_ollama.chat_models import ChatOllama
from langchain.memory import ConversationBufferMemory
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder, SystemMessagePromptTemplate, HumanMessagePromptTemplate
from langchain_core.runnables import RunnableWithMessageHistory

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

# Streamlit framework
st.title('Langchain Demo Chatbot')
input_text = st.text_input("Search for any topics you want...") 


# Defining Prompt Template with message placeholders
prompt = ChatPromptTemplate([
        SystemMessagePromptTemplate.from_template(
            "You are a helpful assistant. Please respond to the user queries"
        ),

        # The variable_name here must align with memory
        MessagesPlaceholder(variable_name="chat_history"),
        HumanMessagePromptTemplate.from_template("{question}")
        
    ]
)

#LLM
llm = ChatOllama(model="qwen2.5-coder:latest")

# String output parser 
output_parser = StrOutputParser()

# Initialize memory
def get_memory(session_id: str):
    if "memory" not in st.session_state:
        st.session_state.memory = {}

    if session_id not in st.session_state.memory:
        st.session_state.memory[session_id] = ConversationBufferMemory(
            memory_key="chat_history", return_messages=True
        )    
    
    return st.session_state.memory[session_id].chat_memory

# memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)


# Creating the chain
chain = prompt | llm | output_parser
chat_chain = RunnableWithMessageHistory(
        runnable=chain,
        get_session_history=get_memory,
        input_messages_key="question",
        history_messages_key="chat_history",
        
)

if input_text:
    # # st.write(chain.invoke({'question':input_text}))
    # response = chain.invoke({'question': input_text})
    # st.write(response['text'])
    # st.write(prompt)

    # 1. Load chat history from memory
    # chat_history = memory.load_memory_variables({})["chat_history"]

    session_id = 'user-session'

    # 2. Run the chain with question + chat history
    response = chat_chain.invoke(
        {"question": input_text}, 
        config={"configurable":{"session_id":session_id}}
        )

    # 3. Show the response in the UI
    # response_str = str(response)
    # st.write(response_str)  

    st.write(response)

    # # 4. Save interaction into memory
    # memory.save_context({"question": input_text }, {"output": response_str})

with st.expander("Conversation History"):
    memory = get_memory("user-session")

    for msg in memory.messages:
        role = type(msg).__name__.replace("Message", "")
        st.write(f"{role}:{msg.content}")    