import json
import os
from typing import Dict, Any
from backend.agents.utils import get_llm, parse_json_response

def run_requirement_agent(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    Requirement Agent (Person 2):
    Analyzes raw user input and generates structured project requirements, user stories,
    functional/non-functional requirements, and an actionable task list.
    """
    user_input = state.get("user_input", "")

    prompt = f"""
You are a senior software engineer analyzing a project requirement.

User requirement: "{user_input}"

Produce a JSON object with exactly these keys:
{{
    "title": "short project title",
    "description": "one paragraph description",
    "user_stories": ["As a user, I want...", ...],
    "functional_requirements": ["The system must...", ...],
    "non_functional_requirements": ["The system should be fast...", ...],
    "tasks": [
        {{"id": 1, "task": "task description", "status": "pending"}},
        ...
    ]
}}

Return ONLY valid JSON, no markdown, no explanation.
"""

    try:
        llm = get_llm(model_name="gpt-4o-mini", temperature=0.2)
        response = llm.invoke(prompt)
        raw_content = response.content if hasattr(response, "content") else str(response)
        parsed = parse_json_response(raw_content)

        state["requirements"] = {
            "title": parsed.get("title", "Project Specification"),
            "description": parsed.get("description", user_input),
            "user_stories": parsed.get("user_stories", []),
            "functional_requirements": parsed.get("functional_requirements", []),
            "non_functional_requirements": parsed.get("non_functional_requirements", [])
        }
        state["tasks"] = parsed.get("tasks", [])
        state["status"] = "REQUIREMENTS_COMPLETED"
        state["logs"].append({
            "agent": "RequirementAgent",
            "message": f"Generated {len(state['requirements']['user_stories'])} user stories and {len(state['tasks'])} tasks."
        })
    except Exception as e:
        # Fallback handling in case of LLM error or JSON parse issue
        state["requirements"] = {
            "title": "Project Specification",
            "description": user_input,
            "user_stories": [f"As a user, I want features implemented for: {user_input}"],
            "functional_requirements": ["Provide API endpoints", "Persist application data"],
            "non_functional_requirements": ["Maintain fast performance", "Modular design"]
        }
        state["tasks"] = [
            {"id": 1, "task": "Set up project boilerplate", "status": "pending"},
            {"id": 2, "task": "Implement core logic", "status": "pending"},
            {"id": 3, "task": "Write test suite", "status": "pending"}
        ]
        state["status"] = "REQUIREMENTS_COMPLETED"
        state["logs"].append({
            "agent": "RequirementAgent",
            "message": f"Requirements parsed with fallback due to notice: {str(e)}"
        })

    return state
