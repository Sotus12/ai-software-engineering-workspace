from typing import Dict, Any

def run_developer_agent(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    Developer Agent (Person 2):
    Generates and writes project code using approved tools (Person 3).
    Includes logic to ingest test error reports during feedback loops.
    """
    retry_count = state.get("retry_count", 0)
    test_results = state.get("test_results", {})
    
    if retry_count > 0 and not test_results.get("passed", True):
        # Developer Agent is responding to failed test feedback
        state["logs"].append({
            "agent": "DeveloperAgent", 
            "message": f"Fixing code errors reported by Testing Agent (Attempt {retry_count}). Errors: {test_results.get('summary', '')}"
        })
    else:
        state["logs"].append({
            "agent": "DeveloperAgent",
            "message": "Generating initial codebase files based on architecture."
        })
        
    state["generated_files"] = ["main.py", "models.py", "database.py", "test_main.py"]
    state["status"] = "DEVELOPMENT_COMPLETED"
    return state
