import json
from typing import Dict, Any
from backend.agents.utils import get_llm, parse_json_response

def run_architecture_agent(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    Architecture Agent (Person 2):
    Designs system architecture including tech stack, directory layout, REST APIs,
    and database schema based on requirements.
    """
    requirements = state.get("requirements", {})

    prompt = f"""
You are a software architect. Design the system architecture for this project.

Requirements:
{json.dumps(requirements, indent=2)}

Return a JSON object with exactly these keys:
{{
    "stack": {{
        "backend": "FastAPI",
        "frontend": "React",
        "database": "SQLite",
        "testing": "PyTest"
    }},
    "structure": ["main.py", "models.py", "database.py", "test_main.py"],
    "apis": [
        {{
            "method": "GET",
            "path": "/items",
            "summary": "Get all items",
            "response": {{"items": "list"}}
        }}
    ],
    "database_schema": [
        {{
            "table": "items",
            "columns": ["id INTEGER PRIMARY KEY", "name TEXT NOT NULL", "done BOOLEAN DEFAULT 0"]
        }}
    ]
}}

Use ONLY: FastAPI, SQLite, PyTest. Return ONLY valid JSON.
"""

    try:
        llm = get_llm(model_name="gpt-4o-mini", temperature=0.2)
        response = llm.invoke(prompt)
        raw_content = response.content if hasattr(response, "content") else str(response)
        parsed = parse_json_response(raw_content)

        state["architecture"] = parsed
        state["status"] = "ARCHITECTURE_COMPLETED"
        state["logs"].append({
            "agent": "ArchitectureAgent",
            "message": f"Designed architecture with {len(parsed.get('apis', []))} API endpoints and {len(parsed.get('structure', []))} files."
        })
    except Exception as e:
        # Fallback architecture
        fallback_arch = {
            "stack": {
                "backend": "FastAPI",
                "frontend": "React",
                "database": "SQLite",
                "testing": "PyTest"
            },
            "structure": ["main.py", "models.py", "database.py", "test_main.py"],
            "apis": [
                {"method": "GET", "path": "/health", "summary": "Health check"},
                {"method": "GET", "path": "/items", "summary": "Get items"},
                {"method": "POST", "path": "/items", "summary": "Create item"}
            ],
            "database_schema": [
                {
                    "table": "items",
                    "columns": ["id INTEGER PRIMARY KEY AUTOINCREMENT", "name TEXT NOT NULL"]
                }
            ]
        }
        state["architecture"] = fallback_arch
        state["status"] = "ARCHITECTURE_COMPLETED"
        state["logs"].append({
            "agent": "ArchitectureAgent",
            "message": f"Designed fallback architecture due to notice: {str(e)}"
        })

    return state
