import pytest
from unittest.mock import patch, mock_open, MagicMock
from claude_task_dispatcher import load_workflow, execute_task, execute_workflow

def test_load_workflow_json():
    """Test loading a JSON workflow."""
    mock_json_content = '{"name": "Test Workflow", "tasks": []}'
    with patch('builtins.open', mock_open(read_data=mock_json_content)) as mock_file:
        workflow = load_workflow('test.json')
        assert workflow['name'] == "Test Workflow"
        mock_file.assert_called_once_with('test.json', 'r')

def test_load_workflow_yaml():
    """Test loading a YAML workflow."""
    mock_yaml_content = """name: Test Workflow
tasks: []"""
    with patch('builtins.open', mock_open(read_data=mock_yaml_content)) as mock_file:
        workflow = load_workflow('test.yml')
        assert workflow['name'] == "Test Workflow"
        mock_file.assert_called_once_with('test.yml', 'r')

def test_execute_task_http_request():
    """Test executing an HTTP request task."""
    task = {
        "name": "Test Task",
        "type": "http_request",
        "method": "GET",
        "url": "http://example.com"
    }
    with patch('requests.request', return_value=MagicMock(status_code=200)) as mock_request:
        execute_task(task)
        mock_request.assert_called_once_with(method="GET", url="http://example.com", headers={}, json={})
