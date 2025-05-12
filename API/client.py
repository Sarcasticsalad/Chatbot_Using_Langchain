import requests
import streamlit as st

# === Streamlit Framework Setup ===
st.title('Langchain Demo Chatbot')
user_input = st.text_input("Search for any topics you want...") 
session_id = "user-session"

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

# === Handle Input and Show Chat ===
if "history" not in st.session_state:
    st.session_state.history = []

if user_input:
    answer = ask_chatbot(user_input, session_id)
    st.session_state.history.append(("You", user_input))
    st.session_state.history.append(("Bot", answer))


# == Display Conversation history ==
for sender, msg in st.session_state.history:
    st.write(f"{sender}: {msg}")    

