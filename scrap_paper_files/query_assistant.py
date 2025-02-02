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
