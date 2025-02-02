# AI Multimodule Project

This project is designed to demonstrate the integration of multiple modules in a single application. It includes various components such as data processing, machine learning, and user interface.

## Architecture
```bash
                        +---------------------+
                        |     Orchestrator    |
                        |  (Task Dispatcher)  |
                        +----------+----------+
                                   |
                  +----------------+----------------+
                  |                |                |
         +--------v--------+ +-----v-------+ +------v------+
         |  Assistant API  | |  Code API   | |   RAG API   |
         |   (FastAPI)     | | (FastAPI)   | | (FastAPI)   |
         +--------+--------+ +-----+-------+ +------^------+
                  |                |                |
                  |                |                |
           +------v------+  +------v-------+  +-----+------+
           |  GPT4All    |  | Code Model   |  | FAISS/LLM  |
           | (Inference) |  |  Engine      |  |  Retrieval |
           +-------------+  +--------------+  +------------+
                              
                               +------------------+
                               | Autonomous API   |
                               |  (FastAPI)       |
                               +------------------+
                                         |
                                         v
                               +------------------+
                               |  Task Queue/     |
                               |  Scheduler (e.g.,|
                               |   asyncio, Celery|
                               |   Redis, etc.)   |
                               +------------------+

```
## Snippets


## Running the embed & ranker services

Now that the files are in the services folder, you must reference them by their module path. From the root of your project (ai_multimodule_project), run:


2.1 For the Embeddings Service
```bash
uvicorn services.local_embeddings_service:app --port 8005 --reload
```

2.2 For the Ranker Service
```bash
uvicorn services.local_ranker_service:app --port 8006 --reload
```

Explanation:

The module name is now services.local_embeddings_service because the file is inside the services directory and Python will look for __init__.py (which we created).
The :app part tells uvicorn to load the app variable from that module.




pip install gpt4all  # if a Python package is available, else follow repo instructions
pip install faiss-cpu  # or faiss-gpu if you want GPU support
<!-- pip install sentence-transformers -->


conda create --name assistant python=3.12
conda activate assistant
conda install -c pytorch -c nvidia faiss-gpu=1.8.0 pytorch pytorch-cuda numpy


conda install -c conda-forge faiss-gpu
conda create --name assistant python=3.12

conda search -c pytorch -c nvidia faiss-gpu pytorch pytorch-cuda numpy
conda install -c pytorch -c nvidia faiss-gpu pytorch pytorch-cuda numpy

conda search -c pytorch -c nvidia  numpy

### Chat agent example

```py
import os
from sentence_transformers import SentenceTransformer
import numpy as np
import faiss
from gpt4all import GPT4All  # Adjust import based on your GPT4All package setup

# -------------------------
# 1. Initialize Embedding Model and FAISS Index
# -------------------------
embedding_model = SentenceTransformer('all-MiniLM-L6-v2')  # A small, fast model

# Define embedding dimension (for all-MiniLM-L6-v2 it is 384)
embedding_dim = 384
faiss_index = faiss.IndexFlatL2(embedding_dim)

# We'll store our conversation history in a list for reference
conversation_history = []  # Each entry: {"text": <str>, "embedding": <np.array>}

# -------------------------
# 2. Initialize GPT4All Model
# -------------------------
# Note: Refer to GPT4All documentation on how to initialize the model properly.
gpt4all_model = GPT4All(model="gpt4all-lora-quantized.bin")  # Adjust model file as needed

# -------------------------
# 3. Functions for Embedding, Memory Update, and Retrieval
# -------------------------
def get_embedding(text: str) -> np.array:
    """Return the embedding vector for the given text."""
    return embedding_model.encode(text, convert_to_numpy=True)

def update_memory(text: str):
    """Generate embedding for new text and add it to the FAISS index and history."""
    emb = get_embedding(text)
    faiss_index.add(np.array([emb]))  # Add a single vector
    conversation_history.append({"text": text, "embedding": emb})

def retrieve_context(query: str, k: int = 3) -> str:
    """Retrieve top-k similar conversation snippets from the FAISS index."""
    query_emb = get_embedding(query)
    D, I = faiss_index.search(np.array([query_emb]), k)
    # Retrieve the text snippets corresponding to indices
    retrieved_texts = [conversation_history[i]["text"] for i in I[0] if i < len(conversation_history)]
    return "\n".join(retrieved_texts)

# -------------------------
# 4. Main Conversation Loop
# -------------------------
def run_assistant():
    print("AI Assistant initialized. Type your message, or 'exit' to quit.")
    while True:
        user_input = input("You: ")
        if user_input.strip().lower() == "exit":
            break

        # Retrieve context from previous conversation snippets
        context = retrieve_context(user_input, k=3) if conversation_history else ""
        prompt = f"Context:\n{context}\n\nUser: {user_input}\nAssistant:"

        # Generate a response using GPT4All
        response = gpt4all_model.generate(prompt)  # Adjust method per your GPT4All API
        print("Assistant:", response)

        # Update memory with both user input and assistant response for future context
        update_memory(f"User: {user_input}")
        update_memory(f"Assistant: {response}")

if __name__ == "__main__":
    run_assistant()
```


## Installation Steps 

1. **Clone the Repository:**
