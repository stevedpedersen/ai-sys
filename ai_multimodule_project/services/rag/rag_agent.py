# services/rag/rag_agent.py
from fastapi import FastAPI
from common.schemas import Task, AgentResponse
import uvicorn

app = FastAPI(title="RAG Agent")

@app.post("/process", response_model=AgentResponse)
async def process(task: Task):
    context = task.payload.get("context", "")
    # Here you would typically query your FAISS index
    # For now, simulate retrieval:
    retrieved_context = f"Retrieved context for: {context}"
    response = AgentResponse(
        task_id=task.task_id,
        status="success",
        data={"retrieved": retrieved_context}
    )
    return response

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8003)
