# code_specialist_agent.py
from fastapi import FastAPI, Request, APIRouter
import uvicorn
# Create an API router
router = APIRouter()


@router.post("/process")
async def process(request: Request):
    data = await request.json()
    code_query = data.get("query", "")
    # Replace this simulation with your code-generation logic.
    response = f"Code Specialist processed your query: {code_query}"
    return {"response": response}

app = FastAPI(title="Code Specialist Agent")
app.include_router(router, prefix="")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8002)