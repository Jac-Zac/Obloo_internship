# Building a chatbot with Chainlit

This code let's you run an LLM through ... With ...

You can see the code of the steps up to the final solution:

- [app.py](app.py) - Answers questions, remembers questions, and supports uploaded text files

### Notes:

- [langsmith](https://www.youtube.com/results?search_query=langsmith): used for tracking chats in the future
- chainlit

### Installation

- Install [Ollama](https://ollama.com/)

- Install the model we are using:

```bash
ollama pull mistral
```

##### Set up a Python virtual environment

```bash
python -m venv .env
source .env/bin/active
```

#### Install dependencies

```bash
pip install -r requirements.txt
```

#### Run the chatbot:

```bash
chainlit run app.py -w -h
```

> Navigate to http://localhost:8000
