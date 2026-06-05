import pytest
from unittest.mock import patch, MagicMock
from commit_message_linter import analyze_commit_message, get_commit_messages

def test_analyze_commit_message():
    mock_response = {
        'choices': [
            {
                'message': {
                    'content': 'This is a well-written commit message.'
                }
            }
        ]
    }

    with patch('commit_message_linter.ChatCompletion.create', return_value=mock_response):
        with patch('commit_message_linter.openai', create=True):
            result = analyze_commit_message("Initial commit", "fake_api_key")
            assert result == "This is a well-written commit message."

def test_get_commit_messages_single_commit():
    mock_repo = MagicMock()
    mock_commit = MagicMock()
    mock_commit.message = "Initial commit"
    mock_repo.commit.return_value = mock_commit

    with patch('commit_message_linter.Repo', return_value=mock_repo):
        result = get_commit_messages("/fake/repo", "abc123")
        assert result == ["Initial commit"]

def test_get_commit_messages_all_commits():
    mock_repo = MagicMock()
    mock_commit1 = MagicMock()
    mock_commit1.message = "Initial commit"
    mock_commit2 = MagicMock()
    mock_commit2.message = "Added new feature"
    mock_repo.iter_commits.return_value = [mock_commit1, mock_commit2]

    with patch('commit_message_linter.Repo', return_value=mock_repo):
        result = get_commit_messages("/fake/repo")
        assert result == ["Initial commit", "Added new feature"]