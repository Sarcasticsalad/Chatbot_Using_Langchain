import requests
import streamlit as st

# === Streamlit Framework Setup ===
st.title('Langchain Demo Chatbot')

# Fixed session ID (can be customized per user in future)
session_id = "user-session"

# === Initialize Streamlit session state ===
if "history" not in st.session_state:
    # Stores conversation tuples (sender, message)
    st.session_state.history = []

if "last_input" not in st.session_state:
    # Avoids resending same message
    st.session_state.last_input = None 

if "last_response" not in st.session_state:
    # Stores last bot response
    st.session_state.last_response = None       

# === Function to call FastAPI backend ===
def ask_chatbot(question: str, session_id: str = "user-session"):
    """
    Sends a question to the chatbot backend and returns the response.

    Args:
        question (str): The user's input message.
        session_id (str): A unique session identifier for memory tracking.

    Returns:
        str: The chatbot's response text.    

    """
    # Endpoint exposed by FastAPI backend
    url = "http://localhost:8000/chat/invoke"

    # Request payload formatted per LangServe's expected schema
    payload = {
        "input": {"question": question},
        "config": {
            "configurable": {"session_id": session_id}
        }
    }
    try:
        response = requests.post(url, json=payload)

        # # Debugging: Check the raw response content
        # st.write(f"Raw Response: {response.text}")

        # Check for successful response
        if response.status_code == 200:
            response_json = response.json()

            # First Layer extraction
            outer_output = response_json.get("output", {})

            # Second layer extraction
            if isinstance(outer_output, dict):
                return outer_output.get("output", "[No output found]")
            else:
                return outer_output

        else:
            return f"Error: {response.status_code} - {response.text}"
    
    except Exception as e:
        return f"request failed: {e}"

# === Sidebar: Reset conversation ===
if st.sidebar.button("New Chat", use_container_width=True):
    st.session_state.history = []
    st.session_state.last_input = None
    st.session_state.last_response = None

# Settings button - can add options later
st.sidebar.button("Settings", use_container_width=True)


# === Chat Input Field  ===
user_input = st.chat_input("Say something") 

if user_input:
    # Avoid resending duplicate input
    if user_input != st.session_state.last_input:
        answer = ask_chatbot(user_input, session_id)

        # Store input and output in session state
        st.session_state.last_input = user_input
        st.session_state.last_response = answer
        st.session_state.history.append(("user", user_input))
        st.session_state.history.append(("assistant", answer))

# == Display Conversation history ==
for sender, msg in st.session_state.history:
    with st.chat_message(sender):
        st.markdown(msg)    

