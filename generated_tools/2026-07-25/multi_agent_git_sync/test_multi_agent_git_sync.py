import os
import pytest
from unittest.mock import patch, MagicMock
from multi_agent_git_sync import lock_file, unlock_file, create_branch, resolve_merge_conflict

def test_lock_file(tmp_path):
    repo_path = tmp_path / "repo"
    repo_path.mkdir()
    file_path = "test_file.py"

    result = lock_file(str(repo_path), file_path, "agent_1")
    assert result == f"File {file_path} locked by agent_1."
    assert os.path.exists(repo_path / f"{file_path}.lock")

def test_unlock_file(tmp_path):
    repo_path = tmp_path / "repo"
    repo_path.mkdir()
    file_path = "test_file.py"
    lock_file_path = repo_path / f"{file_path}.lock"
    lock_file_path.write_text("agent_1")

    result = unlock_file(str(repo_path), file_path)
    assert result == f"File {file_path} unlocked."
    assert not os.path.exists(lock_file_path)

@patch("multi_agent_git_sync.Repo")
def test_create_branch(mock_repo):
    mock_repo.return_value.create_head.return_value = "new_branch"
    result = create_branch("/fake/repo", "new_branch")
    assert result == "Branch new_branch created."
    mock_repo.return_value.create_head.assert_called_once_with("new_branch")