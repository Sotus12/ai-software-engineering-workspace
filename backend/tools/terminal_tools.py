import subprocess
from typing import Dict, Any

def execute_command(command: str, cwd: str = None) -> Dict[str, Any]:
    """
    Execute controlled terminal / test execution command (Person 3).
    Returns stdout, stderr, exit_code.
    """
    try:
        result = subprocess.run(
            command,
            shell=True,
            cwd=cwd,
            capture_output=True,
            text=True,
            timeout=30
        )
        return {
            "stdout": result.stdout,
            "stderr": result.stderr,
            "exit_code": result.returncode,
            "success": result.returncode == 0
        }
    except Exception as e:
        return {
            "stdout": "",
            "stderr": str(e),
            "exit_code": -1,
            "success": False
        }
