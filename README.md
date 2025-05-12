# Chatbot Using LangChain

1) Creating a virtual environment

```
py -3.11 -m venv .venv
```

2) Activate the virtual environment

```
source .venv/Scripts/activate
```

3) Install the packages from requirements.txt file

```
pip install -r requirements.txt
```

4) Creating a .env file

```
# Add the following configurations
LANGSMITH_TRACING=true
LANGSMITH_API_KEY = "Your_Langsmith_API_Key"
LANGSMITH_ENDPOINT="https://api.smith.langchain.com"
LANGCHAIN_PROJECT = "Your_Project_Name"

Note: You can generate the API key from the documentation.

```

5) Setting up Ollama

```
i) Download Ollama and install it on your system.
```

```
ii) Go to command prompt and type ollama to confirm installation.
```

```
iii) Go to the models in the Ollama website and Select your specific model.

Then type run the following command:

ollama run <model_name>
```

6) Running the Chatbot

```
i) Open a terminal and go to the API folder. Then in the terminal run the following command:

    python server.py
```
Note: 
This runs the Langserve + FastAPI configurations. 
The default endpoint for the Chatbot is http://127.0.0.1:8000/chat/invoke

```
ii) Open another terminal and go to the API folder. Then run the following command:

    streamlit run client.py
```

```
iii) Now you can interact with your llm model through an API interface.
```

