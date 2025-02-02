# orchestrator/orchestrator.py
import asyncio
import httpx
import uuid
from common.schemas import Task

async def send_task(url: str, task: Task):
    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=task.dict())
        return response.json()

async def main():
    # Create a unique task ID for each request.
    task_id = str(uuid.uuid4())

    # Build tasks for different agents.
    assistant_task = Task(
        task_id=task_id,
        agent="assistant",
        payload={"input": "What is the weather like today?"}
    )
    code_task = Task(
        task_id=str(uuid.uuid4()),
        agent="code_specialist",
        payload={"query": "Generate a Python function to sort a list."}
    )
    rag_task = Task(
        task_id=str(uuid.uuid4()),
        agent="rag",
        payload={"context": "Previous conversation about sorting algorithms."}
    )
    autonomous_task = Task(
        task_id=str(uuid.uuid4()),
        agent="autonomous",
        payload={"action": "Schedule a reminder for tomorrow."}
    )

    # Define URLs for each service
    urls = {
        "assistant": "http://localhost:8001/process",
        "code_specialist": "http://localhost:8002/process",
        "rag": "http://localhost:8003/process",
        "autonomous": "http://localhost:8004/process",
    }

    # Dispatch tasks concurrently.
    responses = await asyncio.gather(
        send_task(urls["assistant"], assistant_task),
        send_task(urls["code_specialist"], code_task),
        send_task(urls["rag"], rag_task),
        send_task(urls["autonomous"], autonomous_task)
    )

    for response in responses:
        print(response)

if __name__ == "__main__":
    asyncio.run(main())
