# services/code_specialist/code_specialist_agent.py
from fastapi import FastAPI
from common.schemas import Task, AgentResponse
import uvicorn

app = FastAPI(title="Code Specialist Agent")

@app.post("/process", response_model=AgentResponse)
async def process(task: Task):
    query = task.payload.get("query", "")
    # Simulate code generation or analysis
    generated_code = f"# Code generated for: {query}\ndef reverse_string(s):\n    return s[::-1]"
    response = AgentResponse(
        task_id=task.task_id,
        status="success",
        data={"code": generated_code}
    )
    return response

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8002)
