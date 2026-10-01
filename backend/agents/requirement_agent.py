from typing import Dict, Any

def run_requirement_agent(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    Requirement Agent (Person 2):
    Converts raw user prompt into structured requirements, user stories, and task lists.
    """
    user_input = state.get("user_input", "")
    
    # Placeholder structure for Person 2 to implement full prompt logic
    requirements = {
        "title": "Generated Requirement Specification",
        "description": user_input,
        "user_stories": [
            "As a user, I want the core features implemented so that the app meets my needs."
        ],
        "functional_requirements": [
            "Provide REST API endpoints for primary operations.",
            "Persist application data cleanly."
        ],
        "non_functional_requirements": [
            "Maintain fast response times.",
            "Ensure modular code structure."
        ]
    }
    
    tasks = [
        {"id": 1, "task": "Set up project boilerplate", "status": "pending"},
        {"id": 2, "task": "Implement core API logic", "status": "pending"},
        {"id": 3, "task": "Write automated test suite", "status": "pending"}
    ]
    
    state["requirements"] = requirements
    state["tasks"] = tasks
    state["status"] = "REQUIREMENTS_COMPLETED"
    state["logs"].append({"agent": "RequirementAgent", "message": "Successfully parsed requirements and tasks."})
    return state
