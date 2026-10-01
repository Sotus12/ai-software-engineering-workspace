import os
from typing import List, Dict, Any

def read_file(path: str) -> str:
    """Read contents of a file safely (Person 3)."""
    if not os.path.exists(path):
        raise FileNotFoundError(f"File not found: {path}")
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def write_file(path: str, content: str) -> bool:
    """Write content to a file, creating parent directories if needed (Person 3)."""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    return True

def list_files(directory: str) -> List[str]:
    """List relative file paths in directory (Person 3)."""
    files_list = []
    for root, _, files in os.walk(directory):
        for file in files:
            files_list.append(os.path.relpath(os.path.join(root, file), directory))
    return files_list
