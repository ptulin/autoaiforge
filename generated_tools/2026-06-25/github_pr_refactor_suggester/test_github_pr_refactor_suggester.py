import pytest
from unittest.mock import patch, MagicMock
import openai
from github_pr_refactor_suggester import fetch_pr_diff, suggest_refactors

def test_fetch_pr_diff_success():
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.text = "mock diff content"

    with patch("requests.get", return_value=mock_response):
        diff = fetch_pr_diff("mock_token", "user/repo", 42)
        assert diff == "mock diff content"

def test_fetch_pr_diff_failure():
    mock_response = MagicMock()
    mock_response.status_code = 404
    mock_response.reason = "Not Found"

    with patch("requests.get", return_value=mock_response):
        with pytest.raises(ValueError, match="Failed to fetch PR diff: 404 Not Found"):
            fetch_pr_diff("mock_token", "user/repo", 42)

def test_suggest_refactors_success():
    mock_openai_response = MagicMock()
    mock_openai_response.choices = [MagicMock(text="Mock suggestion")]

    with patch("openai.Completion.create", return_value=mock_openai_response):
        suggestions = suggest_refactors("mock diff", "mock_openai_key")
        assert suggestions == "Mock suggestion"

def test_suggest_refactors_failure():
    mock_openai_error = MagicMock()
    mock_openai_error.__class__ = openai.error.OpenAIError

    with patch("openai.Completion.create", side_effect=openai.error.OpenAIError("API error")):
        with pytest.raises(RuntimeError, match="Failed to get suggestions from OpenAI: API error"):
            suggest_refactors("mock diff", "mock_openai_key")