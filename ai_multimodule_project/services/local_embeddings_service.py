# services/local_embeddings_service.py
from fastapi import FastAPI, HTTPException, APIRouter
from pydantic import BaseModel
from sentence_transformers import SentenceTransformer
import uvicorn

# Create an API router
router = APIRouter()

# Load the embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

class EmbeddingRequest(BaseModel):
    text: str

class EmbeddingResponse(BaseModel):
    embedding: list[float]

@router.post("/embed", response_model=EmbeddingResponse)
async def get_embedding(req: EmbeddingRequest):
    try:
        embedding = model.encode(req.text).tolist()
        return EmbeddingResponse(embedding=embedding)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Create the main FastAPI app and include the router under /api
app = FastAPI(title="Local Embeddings Service")
app.include_router(router, prefix="/api")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8005)
