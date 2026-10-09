import subprocess
import os
import shutil
from typing import Dict, Any


def is_docker_available() -> bool:
    """Check if Docker is installed and the daemon is running."""
    result = subprocess.run(
        ["docker", "info"],
        capture_output=True, text=True
    )
    return result.returncode == 0


def inject_dockerfile(project_path: str) -> bool:
    """
    Copy the standard Dockerfile template into the generated project directory.
    Call this before build_image() or run_tests_in_docker().
    """
    template_path = os.path.join(
        os.path.dirname(__file__), "templates", "Dockerfile.template"
    )
    dest_path = os.path.join(project_path, "Dockerfile")

    if os.path.exists(template_path):
        shutil.copy(template_path, dest_path)
    else:
        # Write a sensible default inline
        with open(dest_path, "w") as f:
            f.write(
                "FROM python:3.11-slim\n"
                "WORKDIR /app\n"
                "COPY requirements.txt .\n"
                "RUN pip install --no-cache-dir -r requirements.txt\n"
                "COPY . .\n"
                'CMD ["pytest", "-v", "--tb=short"]\n'
            )
    return True


def build_image(project_path: str, image_tag: str = "generated-project") -> Dict[str, Any]:
    """
    Build a Docker image from the generated project directory.
    A Dockerfile must exist (call inject_dockerfile first).
    """
    if not os.path.exists(os.path.join(project_path, "Dockerfile")):
        inject_dockerfile(project_path)

    result = subprocess.run(
        ["docker", "build", "-t", image_tag, "."],
        cwd=project_path,
        capture_output=True, text=True,
        timeout=300
    )
    return {
        "success": result.returncode == 0,
        "stdout": result.stdout,
        "stderr": result.stderr,
        "image_tag": image_tag
    }


def run_in_docker(project_path: str, command: str, image_tag: str = "generated-project") -> Dict[str, Any]:
    """
    Build and run a command inside an isolated Docker container.
    Container is deleted after execution (--rm).
    Network is disabled (--network none) for security.
    """
    if not is_docker_available():
        return {
            "success": False,
            "error": "Docker is not available on this system."
        }

    build_result = build_image(project_path, image_tag)
    if not build_result["success"]:
        return {
            "success": False,
            "error": f"Docker build failed: {build_result['stderr']}"
        }

    result = subprocess.run(
        ["docker", "run", "--rm", "--network", "none", image_tag] + command.split(),
        capture_output=True, text=True,
        timeout=60
    )
    return {
        "success": result.returncode == 0,
        "stdout": result.stdout,
        "stderr": result.stderr,
        "exit_code": result.returncode
    }


def run_tests_in_docker(project_path: str) -> Dict[str, Any]:
    """
    Run pytest inside a Docker container for full isolation.
    This is the safest way to run generated/untrusted code.
    """
    inject_dockerfile(project_path)
    return run_in_docker(project_path, "pytest -v --tb=short")
