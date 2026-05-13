import pytest
from unittest.mock import patch, Mock
from claude_code_assistant import ClaudeCodeAssistant
import requests

@pytest.fixture
def mock_api_key():
    return "test_api_key"

@pytest.fixture
def assistant(mock_api_key):
    return ClaudeCodeAssistant(api_key=mock_api_key)

def test_suggest_code_empty_prompt(assistant):
    with pytest.raises(ValueError, match="Prompt cannot be empty."):
        assistant.suggest_code("")

@patch("claude_code_assistant.requests.post")
def test_suggest_code_success(mock_post, assistant):
    mock_response = Mock()
    mock_response.json.return_value = {"choices": [{"text": "def fibonacci(n):\n    if n <= 1: return n\n    return fibonacci(n-1) + fibonacci(n-2)"}]}
    mock_response.raise_for_status = Mock()
    mock_post.return_value = mock_response

    result = assistant.suggest_code("Write a Python function to calculate Fibonacci.")
    assert "def fibonacci(n):" in result

@patch("claude_code_assistant.requests.post")
def test_suggest_code_api_error(mock_post, assistant):
    mock_post.side_effect = requests.RequestException("API error")
    result = assistant.suggest_code("Write a Python function to calculate Fibonacci.")
    assert "Error communicating with Claude API" in result