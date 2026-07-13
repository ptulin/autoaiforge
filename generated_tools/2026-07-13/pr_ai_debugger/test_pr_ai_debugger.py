import pytest
from unittest.mock import patch, Mock
import pr_ai_debugger
import openai

def test_analyze_pr_success():
    with patch("requests.get") as mock_get, patch("openai.Completion.create") as mock_openai:
        # Mock GitHub API response
        mock_get.side_effect = [
            Mock(status_code=200, json=lambda: {"diff_url": "https://example.com/diff"}),
            Mock(status_code=200, text="mock diff content")
        ]

        # Mock OpenAI API response
        mock_openai.return_value = Mock(choices=[Mock(text="Mock suggestion")])

        result = pr_ai_debugger.analyze_pr(pr_id="123", repo="user/repo", api_key="fake_api_key")

        assert result["pr_id"] == "123"
        assert result["repo"] == "user/repo"
        assert result["suggestions"] == "Mock suggestion"

def test_analyze_pr_missing_diff_url():
    with patch("requests.get") as mock_get:
        # Mock GitHub API response without diff_url
        mock_get.return_value = Mock(status_code=200, json=lambda: {})

        result = pr_ai_debugger.analyze_pr(pr_id="123", repo="user/repo", api_key="fake_api_key")

        assert "error" in result
        assert result["error"] == "Diff URL not found in pull request data."

def test_analyze_pr_openai_error():
    with patch("requests.get") as mock_get, patch("openai.Completion.create", side_effect=openai.error.OpenAIError("OpenAI API error")) as mock_openai:
        # Mock GitHub API response
        mock_get.side_effect = [
            Mock(status_code=200, json=lambda: {"diff_url": "https://example.com/diff"}),
            Mock(status_code=200, text="mock diff content")
        ]

        result = pr_ai_debugger.analyze_pr(pr_id="123", repo="user/repo", api_key="fake_api_key")

        assert "error" in result
        assert "OpenAI API error" in result["error"]