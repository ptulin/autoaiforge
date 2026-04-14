import pytest
from unittest.mock import patch, mock_open
import json
from claude_task_orchestrator import load_workflow, execute_task, run_workflow

@pytest.fixture
def mock_api_response():
    return {
        "choices": [
            {"text": "Processed output"}
        ]
    }

def test_load_workflow():
    mock_data = {"tasks": [{"name": "Test Task", "prompt_template": "Hello {input}"}]}
    with patch("builtins.open", mock_open(read_data=json.dumps(mock_data))):
        workflow = load_workflow("workflow.json")
        assert workflow == mock_data

def test_execute_task(mock_api_response):
    task = {"name": "Test Task", "prompt_template": "Hello {input}"}
    input_data = "World"
    with patch("requests.post") as mock_post:
        mock_post.return_value.json.return_value = mock_api_response
        mock_post.return_value.status_code = 200
        result = execute_task(task, input_data, "fake_api_key")
        assert result == "Processed output"

def test_run_workflow(mock_api_response):
    workflow = {
        "tasks": [
            {"name": "Task 1", "prompt_template": "Task 1 input: {input}"},
            {"name": "Task 2", "prompt_template": "Task 2 input: {input}"}
        ]
    }
    input_data = "Initial input"
    with patch("requests.post") as mock_post:
        mock_post.return_value.json.return_value = mock_api_response
        mock_post.return_value.status_code = 200
        with patch("pathlib.Path.read_text", return_value=input_data):
            run_workflow(workflow, "input.txt", "fake_api_key")
        assert mock_post.call_count == 2
