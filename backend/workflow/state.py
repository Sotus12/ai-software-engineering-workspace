from typing import TypedDict, List, Dict, Any, Optional

class ProjectState(TypedDict):
    """
    Shared state schema passed between all agents in the multi-agent workflow.
    Defined by Person 1 (Orchestrator).
    """
    project_id: str
    user_input: str
    requirements: Dict[str, Any]
    architecture: Dict[str, Any]
    tasks: List[Dict[str, Any]]
    project_path: str
    generated_files: List[str]
    test_results: Dict[str, Any]
    review_results: Dict[str, Any]
    retry_count: int
    max_retries: int
    status: str
    logs: List[Dict[str, str]]
    error_message: Optional[str]
