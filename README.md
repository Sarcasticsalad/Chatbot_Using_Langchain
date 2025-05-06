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

LANGCHAIN_API_KEY = ""
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
i) Streamlit run app.py
```
