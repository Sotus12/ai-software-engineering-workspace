import os
import uuid
from typing import Dict, Any, List
from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from backend.config import settings
from backend.workflow.state import ProjectState
from backend.workflow.graph import run_orchestrator

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="Multi-Agent Software Engineering Workspace API (Person 1 - Orchestrator)",
    version="1.0.0"
)

# Enable CORS for Frontend integration (Person 4)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory store for project states (In production, replace with DB/Redis)
PROJECT_STORE: Dict[str, ProjectState] = {}

class CreateProjectRequest(BaseModel):
    user_input: str
    max_retries: int = 3

class CreateProjectResponse(BaseModel):
    project_id: str
    status: str
    message: str

@app.get("/")
def read_root():
    return {
        "status": "online",
        "app_name": settings.PROJECT_NAME,
        "version": "1.0.0",
        "role": "Person 1 - Orchestrator & Backend Integration"
    }

@app.post("/api/project/create", response_model=CreateProjectResponse)
def create_project(request: CreateProjectRequest, background_tasks: BackgroundTasks):
    """
    Endpoint for Frontend (Person 4) to submit a new requirement and trigger the orchestrator.
    """
    project_id = str(uuid.uuid4())[:8]
    project_path = os.path.join(settings.PROJECTS_DIR, project_id)
    os.makedirs(project_path, exist_ok=True)
    
    initial_state: ProjectState = {
        "project_id": project_id,
        "user_input": request.user_input,
        "requirements": {},
        "architecture": {},
        "tasks": [],
        "project_path": project_path,
        "generated_files": [],
        "test_results": {},
        "review_results": {},
        "retry_count": 0,
        "max_retries": request.max_retries,
        "status": "INITIALIZED",
        "logs": [{"agent": "Orchestrator", "message": f"Project {project_id} initialized."}],
        "error_message": None
    }
    
    PROJECT_STORE[project_id] = initial_state
    
    # Run orchestrator execution synchronously or background
    def execute_workflow(pid: str):
        try:
            final_state = run_orchestrator(PROJECT_STORE[pid])
            PROJECT_STORE[pid] = final_state
        except Exception as e:
            PROJECT_STORE[pid]["status"] = "FAILED"
            PROJECT_STORE[pid]["error_message"] = str(e)
            PROJECT_STORE[pid]["logs"].append({"agent": "Orchestrator", "message": f"Error: {str(e)}"})

    background_tasks.add_task(execute_workflow, project_id)

    return CreateProjectResponse(
        project_id=project_id,
        status="INITIALIZED",
        message="Project workflow started successfully."
    )

@app.get("/api/project/{project_id}/status")
def get_project_status(project_id: str):
    """
    Retrieve current workflow state and progress logs for the frontend.
    """
    if project_id not in PROJECT_STORE:
        raise HTTPException(status_code=404, detail="Project ID not found")
    return PROJECT_STORE[project_id]

@app.get("/api/projects")
def list_projects():
    """
    List all created projects and their status.
    """
    return [
        {
            "project_id": pid,
            "status": state.get("status"),
            "user_input": state.get("user_input"),
            "retry_count": state.get("retry_count")
        }
        for pid, state in PROJECT_STORE.items()
    ]

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.main:app", host=settings.HOST, port=settings.PORT, reload=True)
