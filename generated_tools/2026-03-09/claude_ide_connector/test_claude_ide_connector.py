import pytest
from unittest.mock import patch, MagicMock
from claude_ide_connector import Client, ClaudeAPIError
import requests

@pytest.fixture
def mock_client():
    return Client(api_key="test_api_key")

@patch("claude_ide_connector.requests.post")
def test_get_suggestions(mock_post, mock_client):
    mock_post.return_value = MagicMock(status_code=200, json=lambda: {"suggestions": ["suggestion1", "suggestion2"]})
    code = "print('Hello World')"
    result = mock_client.get_suggestions(code)
    assert result == {"suggestions": ["suggestion1", "suggestion2"]}
    mock_post.assert_called_once()

@patch("claude_ide_connector.requests.post")
def test_analyze_code(mock_post, mock_client):
    mock_post.return_value = MagicMock(status_code=200, json=lambda: {"analysis": "No issues found"})
    code = "print('Hello World')"
    result = mock_client.analyze_code(code)
    assert result == {"analysis": "No issues found"}
    mock_post.assert_called_once()

@patch("claude_ide_connector.requests.post")
def test_inline_completion(mock_post, mock_client):
    mock_post.return_value = MagicMock(status_code=200, json=lambda: {"completion": "print('Hello World!')"})
    code = "print('Hello"
    cursor_position = 6
    result = mock_client.inline_completion(code, cursor_position)
    assert result == {"completion": "print('Hello World!')"}
    mock_post.assert_called_once()

@patch("claude_ide_connector.requests.post")
def test_empty_code_error(mock_post, mock_client):
    with pytest.raises(ValueError, match="Code input cannot be empty."):
        mock_client.get_suggestions("")
    mock_post.assert_not_called()

@patch("claude_ide_connector.requests.post")
def test_api_error_handling(mock_post, mock_client):
    mock_post.side_effect = requests.exceptions.RequestException("API error")
    with pytest.raises(ClaudeAPIError, match="Error communicating with Claude API: API error"):
        mock_client.get_suggestions("print('Hello World')")
