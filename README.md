# Generative AI Fundamentals with Python

A small, hands-on Python project for learning the building blocks behind generative AI applications. The examples start with direct LLM API calls and gradually introduce conversation memory, local models, retrieval-augmented generation (RAG), and tool-using agents.

The code is intentionally simple and executable. Each script focuses on one idea so you can change the prompt, provider, model, or control flow and observe the result.

## What You Will Learn

- Calling OpenAI and Google Gemini models from Python
- The difference between stateless and stateful conversations
- Switching between cloud and local model providers
- Building a basic RAG pipeline with TF-IDF and cosine similarity
- Giving an LLM access to application functions as tools
- Orchestrating multiple tool calls in an agent loop
- Understanding practical limitations of simple RAG and prompt-based tool calling

## Project Map

### LLM basics

| Script | Topic |
| --- | --- |
| `openai-app.py` | A direct OpenAI chat completion |
| `gemini-app.py` | A direct Gemini content generation request |
| `gemini-app-chat.py` | A Gemini chat session with conversation state managed by the SDK |
| `llm-stateless.py` | A reusable client with no conversation memory |
| `llm-stateful.py` | Conversation history sent back to the model on each turn |
| `llm_client.py` | Shared provider abstraction used by the later examples |

### Local models

| Script | Topic |
| --- | --- |
| `local-app.py` | Calling a model through the LM Studio Python SDK |
| `local-openai-app.py` | Calling LM Studio through its OpenAI-compatible API |

### RAG and agents

| Script | Topic |
| --- | --- |
| `basic_rag.py` | Retrieve relevant text with TF-IDF, then add it to the prompt |
| `rag_limitations.py` | A basic chatbot used to explore the limits of prompt-only knowledge |
| `tool_chatbot.py` | Let the model request calculator, weather, and time tools |
| `basic_agent.py` | Chain several tools together to create an activity plan |

## Requirements

- Python 3.10 or newer
- An OpenAI API key, a Google Gemini API key, or a local LM Studio installation, depending on the example
- For local examples: LM Studio running with a compatible model loaded

## Setup

Create and activate a virtual environment from the project directory.

### Windows PowerShell

```powershell
python -m venv llm
.\llm\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

If PowerShell blocks activation, run the script with the virtual environment interpreter directly:

```powershell
.\llm\Scripts\python.exe openai-app.py
```

## Configuration

Create a `.env` file in the project root. Add only the keys required by the provider you want to use:

```dotenv
OPENAI_API_KEY=your-openai-api-key
GOOGLE_GEMINI_API_KEY=your-google-gemini-api-key
PROVIDER=gemini
LM_STUDIO_HOST=localhost:1234
LM_STUDIO_MODEL=your-loaded-lm-studio-model
```

Do not commit `.env` or API keys. The repository already ignores `.env`.

The shared client in `llm_client.py` supports these provider values:

- `openai`
- `gemini`
- `local`, `lmstudio`, or `ollama` for the OpenAI-compatible LM Studio endpoint

The provider can be selected per call, which is useful when experimenting:

```python
from llm_client import get_llm_response

messages = [{"role": "user", "content": "Explain embeddings simply."}]
response = get_llm_response(messages, provider="gemini")
```

When `provider` is omitted, the client uses `PROVIDER` from `.env` and defaults to `gemini`.

## Running the Examples

Run commands from the project root with the virtual environment active:

```powershell
python openai-app.py
python gemini-app.py
python gemini-app-chat.py
python llm-stateless.py
python llm-stateful.py
python basic_rag.py
python tool_chatbot.py
python basic_agent.py
```

Interactive examples continue until you enter `exit` or `quit`.

For local model examples, start LM Studio first and then run:

```powershell
python local-app.py
python local-openai-app.py
```

## Suggested Learning Path

1. Run `openai-app.py` or `gemini-app.py` to see a single request and response.
2. Compare `llm-stateless.py` with `llm-stateful.py` to understand memory.
3. Read `llm_client.py` and switch the provider passed to `get_llm_response`.
4. Try `local-app.py` after loading a local model in LM Studio.
5. Run `basic_rag.py` and inspect which documents are retrieved for each query.
6. Run `tool_chatbot.py` to see prompt-based tool selection.
7. Run `basic_agent.py` to see several tool calls coordinated in sequence.

## Important Concepts

### Stateless vs. stateful

A stateless request sends only the current user message. A stateful request stores earlier messages and sends selected history with each new request. The model does not remember previous requests by itself; the application supplies the context.

### RAG

The RAG example follows three basic steps:

1. Store source documents.
2. Retrieve documents similar to the user query.
3. Add the retrieved text to the prompt before calling the model.

This is a teaching example, not a production vector database or document-ingestion pipeline.

### Tools and agents

The tool examples use structured JSON requested by the system prompt. The Python application validates the requested tool, executes it, and sends the result back to the model. In production, tool arguments should be validated carefully and dangerous operations should never be executed blindly.

## Notes

- Model names and API behavior can change. Update the model constants in the scripts if a provider retires a model.
- The examples print raw responses to make the request flow visible.
- `llm_client.py` uses the OpenAI-compatible API for LM Studio; the local server and model must be available before running local provider examples.