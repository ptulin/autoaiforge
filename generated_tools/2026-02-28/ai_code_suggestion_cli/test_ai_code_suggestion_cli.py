import pytest
from unittest.mock import patch, MagicMock
import requests
from ai_code_suggestion_cli import get_code_suggestion

def test_get_code_suggestion_success():
    api_key = "test_api_key"
    description = "function to add two numbers"
    language = "python"

    mock_response = {
        "choices": [
            {"text": "def add(a, b):\n    return a + b"}
        ]
    }

    with patch("requests.post") as mock_post:
        mock_post.return_value = MagicMock(status_code=200, json=lambda: mock_response)
        suggestion = get_code_suggestion(api_key, description, language)
        assert suggestion == "def add(a, b):\n    return a + b"

def test_get_code_suggestion_no_api_key():
    with pytest.raises(ValueError, match="API key is required to fetch code suggestions."):
        get_code_suggestion(None, "function to add two numbers", "python")

def test_get_code_suggestion_api_error():
    api_key = "test_api_key"
    description = "function to add two numbers"
    language = "python"

    with patch("requests.post", side_effect=requests.RequestException("API error")) as mock_post:
        with pytest.raises(requests.RequestException, match="Failed to fetch code suggestion: API error"):
            get_code_suggestion(api_key, description, language)