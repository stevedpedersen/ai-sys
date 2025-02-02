# verify that the 4 models to run Continue locally (chat, auto complete/code, embedding, and reranker) are working correctly by reading in all the project files for this project so far and verify by explaining things.

import torch
from transformers import AutoModelForSequenceClassification, AutoTokenizer

# Assuming 'chat_model' is a simple sequence classification model
tokenizer = AutoTokenizer.from_pretrained('model_name')
model = AutoModelForSequenceClassification.from_pretrained('model_name')

def run_chat(input_text):
    inputs = tokenizer.encode_plus(input_text, 
                                    add_special_tokens=True,
                                    max_length=512,
                                    return_attention_mask=True,
                                    return_tensors='pt',
                                    )
    outputs = model(inputs['input_ids'], attention_mask=inputs['attention_mask'])
    logits = torch.nn.functional.softmax(outputs.logits, dim=-1)
    
    # Get the index of the highest confidence class
    _, predicted_class_idx = torch.max(logits, 1)

    return predicted_class_idx.item()

# Run chat with a few inputs to verify it's working correctly
print(run_chat('How are you doing?'))

# uvicorn services.local_embeddings_service:app --port 8005 --reload && uvicorn services.local_ranker_service:app --port 8006 --reload
