import requests
import streamlit as st

# === Streamlit Framework Setup ===
st.title('Langchain Demo Chatbot')
session_id = "user-session"

# === Session state initialization ===
if "history" not in st.session_state:
    st.session_state.history = []

if "last_input" not in st.session_state:
    st.session_state.last_input = None 

if "last_response" not in st.session_state:
    st.session_state.last_response = None       

# === Backend call function ===
def ask_chatbot(question: str, session_id: str = "user-session"):
    url = "http://localhost:8000/chat/invoke"
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

# === Sidebar ===
if st.sidebar.button("New Chat", use_container_width=True):
    st.session_state.history = []
    st.session_state.last_input = None
    st.session_state.last_response = None

st.sidebar.button("Settings", use_container_width=True)


# === Handle Input  ===
user_input = st.chat_input("Say something") 

if user_input:
    # Only call backend if input is new
    if user_input != st.session_state.last_input:
        answer = ask_chatbot(user_input, session_id)
        st.session_state.last_input = user_input
        st.session_state.last_response = answer
        st.session_state.history.append(("user", user_input))
        st.session_state.history.append(("assistant", answer))

# == Display Conversation history ==
for sender, msg in st.session_state.history:
    with st.chat_message(sender):
        st.markdown(msg)    

