import pytest
from unittest.mock import patch, mock_open
import json
from workflow_ai_automator import execute_workflow

def test_execute_workflow_success():
    workflow = {
        "steps": [
            {"task": "summarize", "input": "Summarize this text."}
        ]
    }
    mock_response = {
        "choices": [{"text": "Summary of the text."}]
    }

    with patch("builtins.open", mock_open(read_data=json.dumps(workflow))):
        with patch("requests.post") as mock_post:
            mock_post.return_value.status_code = 200
            mock_post.return_value.json.return_value = mock_response

            result = execute_workflow("workflow.json", "test_api_key")

            assert len(result["logs"]) == 1
            assert "Task 'summarize' completed successfully." in result["logs"]
            assert len(result["outputs"]) == 1
            assert result["outputs"][0]["output"] == "Summary of the text."

def test_execute_workflow_file_not_found():
    result = execute_workflow("nonexistent.json", "test_api_key")

    assert len(result["logs"]) == 1
    assert "Workflow file 'nonexistent.json' not found." in result["logs"]
    assert len(result["outputs"]) == 0

def test_execute_workflow_invalid_format():
    invalid_workflow = {"invalid": "data"}

    with patch("builtins.open", mock_open(read_data=json.dumps(invalid_workflow))):
        result = execute_workflow("workflow.json", "test_api_key")

        assert len(result["logs"]) == 1
        assert "Invalid workflow file format:" in result["logs"][0]
        assert len(result["outputs"]) == 0
