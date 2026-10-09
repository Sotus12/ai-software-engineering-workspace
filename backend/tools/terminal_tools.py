import subprocess
import re
from typing import Dict, Any


def execute_command(command: str, cwd: str = None, timeout: int = 60) -> Dict[str, Any]:
    """
    Execute a shell command and return structured output.

    Args:
        command: Shell command to run
        cwd:     Working directory (must be inside backend/projects/)
        timeout: Max seconds to wait (default 60)

    Returns:
        {"stdout": str, "stderr": str, "exit_code": int, "success": bool}
    """
    try:
        result = subprocess.run(
            command,
            shell=True,
            cwd=cwd,
            capture_output=True,
            text=True,
            timeout=timeout
        )
        return {
            "stdout": result.stdout,
            "stderr": result.stderr,
            "exit_code": result.returncode,
            "success": result.returncode == 0
        }
    except subprocess.TimeoutExpired:
        return {
            "stdout": "",
            "stderr": f"Command timed out after {timeout} seconds.",
            "exit_code": -1,
            "success": False
        }
    except Exception as e:
        return {
            "stdout": "",
            "stderr": str(e),
            "exit_code": -1,
            "success": False
        }


def install_dependencies(project_path: str) -> Dict[str, Any]:
    """
    Run pip install -r requirements.txt in the given project directory.
    Called by the Testing Agent before running tests.
    Uses a longer timeout since installs can take time.
    """
    return execute_command(
        "pip install -r requirements.txt",
        cwd=project_path,
        timeout=120
    )


def run_tests(project_path: str) -> Dict[str, Any]:
    """
    Run the pytest test suite in the given project directory.
    Returns structured test results for the Testing Agent.

    Returns:
        {
            "passed": bool,
            "stdout": str,
            "stderr": str,
            "exit_code": int,
            "summary": str    # e.g. "5 passed, 1 failed in 0.32s"
        }
    """
    result = execute_command(
        "pytest -v --tb=short",
        cwd=project_path,
        timeout=60
    )

    passed = result["exit_code"] == 0
    summary = _extract_pytest_summary(result["stdout"]) or (
        "All tests passed." if passed else "Tests failed. See stdout for details."
    )

    return {
        "passed": passed,
        "stdout": result["stdout"],
        "stderr": result["stderr"],
        "exit_code": result["exit_code"],
        "summary": summary
    }


def _extract_pytest_summary(output: str) -> str:
    """Parse the final summary line from pytest output."""
    for line in reversed(output.splitlines()):
        line = line.strip()
        if any(word in line for word in ["passed", "failed", "error", "no tests"]):
            # Strip ANSI color codes if present
            clean = re.sub(r'\x1b\[[0-9;]*m', '', line)
            return clean
    return ""
