import pytest
from unittest.mock import patch, MagicMock
import os
import json
from repo_commit_analyzer import analyze_repository, generate_visualizations

@pytest.fixture
def mock_repo():
    mock_repo = MagicMock()
    mock_commit1 = MagicMock()
    mock_commit1.committed_date = 1672531200  # 2023-01-01
    mock_commit1.author.name = "Alice"

    mock_commit2 = MagicMock()
    mock_commit2.committed_date = 1672617600  # 2023-01-02
    mock_commit2.author.name = "Bob"

    mock_commit3 = MagicMock()
    mock_commit3.committed_date = 1672617600  # 2023-01-02
    mock_commit3.author.name = "Alice"

    mock_repo.iter_commits.return_value = [mock_commit1, mock_commit2, mock_commit3]
    mock_repo.bare = False
    return mock_repo

@patch("repo_commit_analyzer.os.path.exists", return_value=True)
@patch("repo_commit_analyzer.Repo")
def test_analyze_repository(mock_repo_class, mock_path_exists, mock_repo):
    mock_repo_class.return_value = mock_repo

    analysis = analyze_repository("/fake/repo/path")

    assert "commit_frequency" in analysis
    assert "contributor_activity" in analysis

    assert analysis["commit_frequency"] == {
        "dates": ["2023-01-01", "2023-01-02"],
        "counts": [1, 2]
    }

    assert analysis["contributor_activity"] == {
        "Alice": 2,
        "Bob": 1
    }

def test_generate_visualizations(tmp_path):
    analysis = {
        "commit_frequency": {
            "dates": ["2023-01-01", "2023-01-02"],
            "counts": [1, 2]
        },
        "contributor_activity": {
            "Alice": 2,
            "Bob": 1
        }
    }

    output_dir = tmp_path / "test_visualizations"
    os.makedirs(output_dir, exist_ok=True)

    generate_visualizations(analysis, str(output_dir))

    assert os.path.exists(output_dir / "commit_frequency.png")
    assert os.path.exists(output_dir / "contributor_activity.png")

@patch("repo_commit_analyzer.os.path.exists", return_value=False)
def test_analyze_repository_invalid_path(mock_path_exists):
    with pytest.raises(FileNotFoundError, match="Repository path '/invalid/repo/path' does not exist."):
        analyze_repository("/invalid/repo/path")

@patch("repo_commit_analyzer.os.path.exists", return_value=True)
@patch("repo_commit_analyzer.Repo")
def test_analyze_repository_bare_repo(mock_repo_class, mock_path_exists):
    mock_repo = MagicMock()
    mock_repo.bare = True
    mock_repo_class.return_value = mock_repo

    with pytest.raises(ValueError, match="The repository is bare and has no commit history."):
        analyze_repository("/fake/repo/path")

@patch("repo_commit_analyzer.os.path.exists", return_value=True)
@patch("repo_commit_analyzer.Repo")
def test_analyze_repository_empty_repo(mock_repo_class, mock_path_exists):
    mock_repo = MagicMock()
    mock_repo.bare = False
    mock_repo.iter_commits.return_value = []
    mock_repo_class.return_value = mock_repo

    analysis = analyze_repository("/fake/repo/path")

    assert analysis == {
        "commit_frequency": {
            "dates": [],
            "counts": []
        },
        "contributor_activity": {}
    }
