import pytest
from unittest.mock import patch, Mock
from llm_code_review_assistant import fetch_pr_files, analyze_code_with_llm

def test_fetch_pr_files_github():
    with patch("llm_code_review_assistant.requests.get") as mock_get:
        mock_response = Mock()
        mock_response.json.return_value = [
            {"patch": "diff --git a/file1.py b/file1.py\n+print('Hello World')"}
        ]
        mock_response.status_code = 200
        mock_get.return_value = mock_response

        files = fetch_pr_files("https://github.com/user/repo", 123)
        assert len(files) == 1
        assert "print('Hello World')" in files[0]

def test_fetch_pr_files_gitlab():
    with patch("llm_code_review_assistant.requests.get") as mock_get:
        mock_response = Mock()
        mock_response.json.return_value = {
            "changes": [
                {"diff": "diff --git a/file1.py b/file1.py\n+print('Hello World')"}
            ]
        }
        mock_response.status_code = 200
        mock_get.return_value = mock_response

        files = fetch_pr_files("https://gitlab.com/user/repo", 123)
        assert len(files) == 1
        assert "print('Hello World')" in files[0]

def test_analyze_code_with_llm():
    with patch("llm_code_review_assistant.openai.Completion.create") as mock_create:
        mock_create.return_value = Mock(choices=[Mock(text="This code looks fine.")])

        suggestions = analyze_code_with_llm(["print('Hello World')"], "fake_api_key")
        assert "file_1" in suggestions
        assert suggestions["file_1"] == "This code looks fine."