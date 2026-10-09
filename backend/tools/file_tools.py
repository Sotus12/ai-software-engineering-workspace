import os
import shutil
from typing import List

# All file operations must stay inside this directory
SAFE_ROOT = os.path.abspath("backend/projects")


def _validate_path(path: str) -> str:
    """
    Reject any path that escapes the safe project sandbox.
    Always call this before any file operation.
    """
    abs_path = os.path.abspath(path)
    if not abs_path.startswith(SAFE_ROOT):
        raise PermissionError(
            f"Access denied: '{path}' is outside the allowed directory '{SAFE_ROOT}'."
        )
    return abs_path


def create_directory(path: str) -> bool:
    """Create a directory (and any parents) inside the safe root."""
    validated = _validate_path(path)
    os.makedirs(validated, exist_ok=True)
    return True


def write_file(path: str, content: str) -> bool:
    """
    Write content to a file inside the safe root.
    Creates parent directories automatically.
    """
    validated = _validate_path(path)
    parent = os.path.dirname(validated)
    if parent:
        os.makedirs(parent, exist_ok=True)
    with open(validated, "w", encoding="utf-8") as f:
        f.write(content)
    return True


def read_file(path: str) -> str:
    """Read and return the content of a file inside the safe root."""
    validated = _validate_path(path)
    if not os.path.exists(validated):
        raise FileNotFoundError(f"File not found: '{path}'")
    with open(validated, "r", encoding="utf-8") as f:
        return f.read()


def edit_file(path: str, old_content: str, new_content: str) -> bool:
    """
    Find and replace a specific block of text in a file.
    Raises ValueError if old_content is not found.
    """
    current = read_file(path)
    if old_content not in current:
        raise ValueError(f"Content to replace not found in '{path}'.")
    updated = current.replace(old_content, new_content, 1)
    write_file(path, updated)
    return True


def list_files(directory: str) -> List[str]:
    """
    Return a list of file paths (relative to directory) inside the given directory.
    """
    validated = _validate_path(directory)
    if not os.path.isdir(validated):
        raise NotADirectoryError(f"Not a directory: '{directory}'")
    result = []
    for root, _, files in os.walk(validated):
        for file in files:
            abs_file = os.path.join(root, file)
            result.append(os.path.relpath(abs_file, validated))
    return result


def delete_file(path: str) -> bool:
    """Delete a single file inside the safe root."""
    validated = _validate_path(path)
    if not os.path.exists(validated):
        raise FileNotFoundError(f"File not found: '{path}'")
    os.remove(validated)
    return True


def delete_directory(path: str) -> bool:
    """Delete a directory and all its contents inside the safe root."""
    validated = _validate_path(path)
    if not os.path.exists(validated):
        raise FileNotFoundError(f"Directory not found: '{path}'")
    shutil.rmtree(validated)
    return True
