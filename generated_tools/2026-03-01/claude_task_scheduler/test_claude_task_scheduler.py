import pytest
from unittest.mock import patch, mock_open, MagicMock
import httpx
import json
from claude_task_scheduler import create_task, load_config

def test_create_task_success():
    mock_response = {"task_id": "12345", "status": "scheduled"}

    with patch("httpx.post") as mock_post:
        mock_http_response = MagicMock()
        mock_http_response.status_code = 200
        mock_http_response.json.return_value = mock_response
        mock_http_response.raise_for_status = MagicMock()
        mock_post.return_value = mock_http_response

        result = create_task("test_task", "24h", "Test prompt", None, "http://mockapi.com", "mock_api_key")
        assert result == mock_response

def test_create_task_api_error():
    with patch("httpx.post") as mock_post:
        mock_http_response = MagicMock()
        mock_http_response.status_code = 400
        mock_http_response.text = "Bad Request"
        mock_http_response.raise_for_status.side_effect = httpx.HTTPStatusError("Bad Request", request=None, response=mock_http_response)
        mock_post.return_value = mock_http_response

        with pytest.raises(RuntimeError, match="API returned an error: Bad Request"):
            create_task("test_task", "24h", "Test prompt", None, "http://mockapi.com", "mock_api_key")

def test_load_config_success():
    mock_yaml = """
    task_name: test_task
    interval: 24h
    prompt: Test prompt
    output: test_output.json
    """
    with patch("builtins.open", mock_open(read_data=mock_yaml)):
        config = load_config("mock_config.yaml")
        assert config["task_name"] == "test_task"
        assert config["interval"] == "24h"
        assert config["prompt"] == "Test prompt"
        assert config["output"] == "test_output.json"

def test_load_config_file_not_found():
    with pytest.raises(FileNotFoundError):
        load_config("nonexistent.yaml")

def test_load_config_invalid_yaml():
    invalid_yaml = "invalid: [unclosed"
    with patch("builtins.open", mock_open(read_data=invalid_yaml)):
        with pytest.raises(ValueError, match="Error parsing YAML configuration"):
            load_config("invalid.yaml")