import os
import pytest
import shutil
from backend.tools.file_tools import (
    write_file, read_file, edit_file, list_files,
    create_directory, delete_file, delete_directory
)
from backend.tools.terminal_tools import execute_command, run_tests

TEST_DIR = "backend/projects/test_tool_suite"


@pytest.fixture(autouse=True)
def cleanup():
    if os.path.exists(TEST_DIR):
        shutil.rmtree(TEST_DIR)
    os.makedirs(TEST_DIR, exist_ok=True)
    yield
    if os.path.exists(TEST_DIR):
        shutil.rmtree(TEST_DIR)


# ── file_tools ────────────────────────────────────────────

def test_create_directory():
    path = os.path.join(TEST_DIR, "subdir")
    assert create_directory(path) is True
    assert os.path.isdir(path)

def test_write_and_read_file():
    path = os.path.join(TEST_DIR, "hello.txt")
    write_file(path, "hello world")
    assert read_file(path) == "hello world"

def test_write_creates_parent_dirs():
    path = os.path.join(TEST_DIR, "nested", "dir", "file.txt")
    write_file(path, "deep content")
    assert read_file(path) == "deep content"

def test_edit_file():
    path = os.path.join(TEST_DIR, "edit.txt")
    write_file(path, "foo bar baz")
    edit_file(path, "bar", "REPLACED")
    assert read_file(path) == "foo REPLACED baz"

def test_edit_file_raises_when_content_not_found():
    path = os.path.join(TEST_DIR, "edit.txt")
    write_file(path, "hello")
    with pytest.raises(ValueError):
        edit_file(path, "NONEXISTENT", "x")

def test_list_files():
    write_file(os.path.join(TEST_DIR, "a.py"), "x")
    write_file(os.path.join(TEST_DIR, "b.py"), "y")
    files = list_files(TEST_DIR)
    assert "a.py" in files
    assert "b.py" in files

def test_delete_file():
    path = os.path.join(TEST_DIR, "del.txt")
    write_file(path, "bye")
    delete_file(path)
    assert not os.path.exists(path)

def test_delete_directory():
    sub = os.path.join(TEST_DIR, "subdir")
    create_directory(sub)
    write_file(os.path.join(sub, "file.txt"), "x")
    delete_directory(sub)
    assert not os.path.exists(sub)

# ── CRITICAL SAFETY TESTS ────────────────────────────────

def test_safety_blocks_parent_traversal():
    """Path traversal attacks must be blocked."""
    with pytest.raises(PermissionError):
        read_file("../../etc/passwd")

def test_safety_blocks_absolute_path_outside_root():
    """Absolute paths outside safe root must be rejected."""
    with pytest.raises(PermissionError):
        write_file("/tmp/evil.txt", "hacked")

def test_safety_blocks_dotdot_in_path():
    with pytest.raises(PermissionError):
        write_file("backend/projects/../../../evil.txt", "bad")

def test_safety_blocks_create_directory_outside_root():
    with pytest.raises(PermissionError):
        create_directory("/tmp/evil_dir")

# ── terminal_tools ────────────────────────────────────────

def test_execute_command_success():
    result = execute_command("echo hello")
    assert result["success"] is True
    assert "hello" in result["stdout"]

def test_execute_command_failure():
    result = execute_command("python -c \"import sys; sys.exit(1)\"")
    assert result["success"] is False
    assert result["exit_code"] == 1

def test_execute_command_timeout():
    result = execute_command("python -c \"import time; time.sleep(10)\"", timeout=1)
    assert result["success"] is False
    assert "timed out" in result["stderr"].lower()
