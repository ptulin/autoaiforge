import pytest
from unittest.mock import patch, MagicMock
from claude_conversation_logger import ClaudeConversationLogger

@pytest.fixture
def mock_logger():
    return ClaudeConversationLogger(api_key="test_api_key")

@patch("claude_conversation_logger.ChatCompletion.create")
def test_interact_with_claude(mock_create, mock_logger):
    mock_create.return_value = MagicMock(choices=[MagicMock(message={"content": "Test response"})])
    response = mock_logger.interact_with_claude("Test prompt")
    assert response == "Test response"

def test_log_interaction(mock_logger):
    mock_logger.log_interaction("Test prompt", "Test response", "test_tag")
    assert len(mock_logger.logs) == 1
    assert mock_logger.logs[0]["prompt"] == "Test prompt"
    assert mock_logger.logs[0]["response"] == "Test response"
    assert mock_logger.logs[0]["tags"] == "test_tag"

def test_export_logs(mock_logger, tmp_path):
    mock_logger.log_interaction("Test prompt", "Test response", "test_tag")
    csv_path = tmp_path / "logs.csv"
    json_path = tmp_path / "logs.json"

    mock_logger.export_logs(csv_path, "csv")
    assert csv_path.exists()

    mock_logger.export_logs(json_path, "json")
    assert json_path.exists()