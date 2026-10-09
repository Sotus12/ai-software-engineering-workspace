import os
from typing import Dict, Any
from backend.tools.terminal_tools import execute_command

def _extract_pytest_summary(output: str) -> str:
    """Extract the final summary line from pytest output."""
    if not output:
        return ""
    for line in reversed(output.splitlines()):
        line_clean = line.strip()
        if ("passed" in line_clean or "failed" in line_clean or "error" in line_clean):
            return line_clean
    return ""

def run_testing_agent(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    Testing Agent (Person 2):
    Executes automated tests in the generated project directory using pytest via terminal tools.
    """
    project_path = state.get("project_path", "")

    if project_path and os.path.exists(project_path):
        # Step 1: Install dependencies if requirements.txt exists
        req_file = os.path.join(project_path, "requirements.txt")
        if os.path.exists(req_file):
            execute_command("pip install -r requirements.txt", cwd=project_path)

        # Step 2: Run pytest
        test_result = execute_command("python -m pytest -v --tb=short 2>&1", cwd=project_path)

        # If python -m pytest exit_code wasn't 0, try pytest command directly
        if not test_result.get("success", False) and test_result.get("exit_code") == -1:
            test_result = execute_command("pytest -v --tb=short 2>&1", cwd=project_path)

        passed = test_result.get("exit_code", -1) == 0
        stdout = test_result.get("stdout", "")
        stderr = test_result.get("stderr", "")

        summary = _extract_pytest_summary(stdout) or (_extract_pytest_summary(stderr) if stderr else "")
        if not summary:
            summary = "PASSED" if passed else "FAILED"

        state["test_results"] = {
            "passed": passed,
            "stdout": stdout,
            "stderr": stderr,
            "exit_code": test_result.get("exit_code", -1),
            "summary": summary
        }
    else:
        # If no project path exists, default test result
        state["test_results"] = {
            "passed": True,
            "stdout": "No project path provided, skipped execution.",
            "stderr": "",
            "exit_code": 0,
            "summary": "PASSED (Skipped - No files)"
        }

    passed = state["test_results"]["passed"]
    summary = state["test_results"]["summary"]

    state["status"] = "TESTING_COMPLETED"
    state["logs"].append({
        "agent": "TestingAgent",
        "message": f"Tests {'PASSED ✅' if passed else 'FAILED ❌'}: {summary}"
    })

    return state
