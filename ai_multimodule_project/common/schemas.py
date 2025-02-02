# common/schemas.py
from pydantic import BaseModel, Field
from typing import Optional, List

class Task(BaseModel):
    task_id: str = Field(..., description="Unique identifier for the task")
    agent: str = Field(..., description="The target agent, e.g., 'assistant', 'code', 'rag', 'autonomous'")
    payload: dict = Field(..., description="Agent-specific input data")
    priority: Optional[int] = Field(1, description="Priority of the task (1=high, larger=lower)")

class AgentResponse(BaseModel):
    task_id: str = Field(..., description="The task id this response is addressing")
    status: str = Field(..., description="e.g., 'success', 'error'")
    data: Optional[dict] = Field(None, description="Agent-specific response data")
    error: Optional[str] = Field(None, description="Error message, if any")

class OrchestratorRequest(BaseModel):
    tasks: List[Task] = Field(..., description="List of tasks to dispatch")
