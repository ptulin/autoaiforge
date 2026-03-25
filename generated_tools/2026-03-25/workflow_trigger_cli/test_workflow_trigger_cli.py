import pytest
import json
from unittest.mock import patch, MagicMock
from workflow_trigger_cli import trigger_workflow, monitor_workflow

def test_trigger_workflow_success():
    mock_response = MagicMock()
    mock_response.json.return_value = {"workflow_id": "12345"}
    mock_response.status_code = 200
    
    with patch('requests.post', return_value=mock_response):
        result = trigger_workflow("test_workflow", {"key": "value"}, retries=0, delay=1)
        assert result["workflow_id"] == "12345"

def test_trigger_workflow_failure():
    with patch('requests.post', side_effect=Exception("Network error")):
        with pytest.raises(Exception, match="Network error"):
            trigger_workflow("test_workflow", {"key": "value"}, retries=0, delay=1)

def test_monitor_workflow_success():
    mock_response_running = MagicMock()
    mock_response_running.json.return_value = {"status": "running"}
    mock_response_running.status_code = 200

    mock_response_completed = MagicMock()
    mock_response_completed.json.return_value = {"status": "completed", "result": "success"}
    mock_response_completed.status_code = 200

    with patch('requests.get', side_effect=[mock_response_running, mock_response_completed]):
        result = monitor_workflow("12345")
        assert result["status"] == "completed"
        assert result["result"] == "success"

def test_monitor_workflow_failure():
    mock_response_running = MagicMock()
    mock_response_running.json.return_value = {"status": "running"}
    mock_response_running.status_code = 200

    mock_response_failed = MagicMock()
    mock_response_failed.json.return_value = {"status": "failed"}
    mock_response_failed.status_code = 200

    with patch('requests.get', side_effect=[mock_response_running, mock_response_failed]):
        with pytest.raises(Exception, match="Workflow execution failed."):
            monitor_workflow("12345")