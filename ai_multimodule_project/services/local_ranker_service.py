# services/local_ranker_service.py
from fastapi import FastAPI, HTTPException, APIRouter
from pydantic import BaseModel
from sentence_transformers import SentenceTransformer, util
import uvicorn
from typing import List

router = APIRouter()

# Load the model (using the same model here)
model = SentenceTransformer("all-MiniLM-L6-v2")

class RankerRequest(BaseModel):
    query: str
    candidates: List[str]

class CandidateScore(BaseModel):
    candidate: str
    score: float

class RankerResponse(BaseModel):
    results: List[CandidateScore]

@router.post("/rank", response_model=RankerResponse)
async def rank_candidates(req: RankerRequest):
    try:
        query_embedding = model.encode(req.query, convert_to_tensor=True)
        candidate_embeddings = model.encode(req.candidates, convert_to_tensor=True)
        scores = util.cos_sim(query_embedding, candidate_embeddings)[0]
        results = [
            CandidateScore(candidate=c, score=s)
            for c, s in zip(req.candidates, scores.tolist())
        ]
        results = sorted(results, key=lambda x: x.score, reverse=True)
        return RankerResponse(results=results)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

app = FastAPI(title="Local Ranker Service")
app.include_router(router, prefix="/api")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8006)
