# services/assistant/assistant_agent.py
from fastapi import FastAPI, Request
from common.schemas import Task, AgentResponse
import uvicorn
import uuid

app = FastAPI(title="Assistant Agent")

@app.post("/process", response_model=AgentResponse)
async def process(task: Task):
    # Simulate processing with GPT4All
    input_text = task.payload.get("input", "")
    # For demonstration: generate a response using the input text.
    generated_response = f"Assistant processed: {input_text}"
    response = AgentResponse(
        task_id=task.task_id,
        status="success",
        data={"response": generated_response}
    )
    return response

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)
