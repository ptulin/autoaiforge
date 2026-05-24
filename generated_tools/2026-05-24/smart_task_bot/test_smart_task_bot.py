import pytest
import json
from unittest.mock import patch, mock_open
from smart_task_bot import load_tasks, execute_task, execute_api_call, execute_ai_agent, execute_file_io

def test_load_tasks_valid():
    mock_data = '[{"type": "api_call", "url": "http://example.com"}]'
    with patch("builtins.open", mock_open(read_data=mock_data)):
        tasks = load_tasks("tasks.json")
        assert tasks == [{"type": "api_call", "url": "http://example.com"}]

def test_load_tasks_invalid_json():
    mock_data = '{invalid json}'
    with patch("builtins.open", mock_open(read_data=mock_data)):
        with pytest.raises(ValueError, match="not a valid JSON file"):
            load_tasks("tasks.json")

def test_execute_api_call_success():
    task = {
        "type": "api_call",
        "url": "http://example.com",
        "method": "GET"
    }
    mock_response = {"key": "value"}
    with patch("requests.request") as mock_request:
        mock_request.return_value.json.return_value = mock_response
        mock_request.return_value.raise_for_status = lambda: None
        result = execute_api_call(task)
        assert result == mock_response

def test_execute_ai_agent_success():
    task = {
        "type": "ai_agent",
        "api_key": "fake_api_key",
        "prompt": "Hello, AI!",
        "model": "text-davinci-003",
        "max_tokens": 10
    }
    mock_response = {"choices": [{"text": "Hello, world!"}]}
    with patch("openai.Completion.create") as mock_create:
        mock_create.return_value = mock_response
        result = execute_ai_agent(task)
        assert result == "Hello, world!"

def test_execute_file_io_read():
    task = {
        "type": "file_io",
        "operation": "read",
        "file_path": "test.txt"
    }
    mock_data = "file content"
    with patch("builtins.open", mock_open(read_data=mock_data)) as mock_file:
        result = execute_file_io(task)
        assert result == "file content"
        mock_file.assert_called_once_with("test.txt", 'r')

def test_execute_file_io_write():
    task = {
        "type": "file_io",
        "operation": "write",
        "file_path": "test.txt",
        "content": "new content"
    }
    with patch("builtins.open", mock_open()) as mock_file:
        result = execute_file_io(task)
        assert result == "Content written to test.txt"
        mock_file.assert_called_once_with("test.txt", 'w')
        mock_file().write.assert_called_once_with("new content")