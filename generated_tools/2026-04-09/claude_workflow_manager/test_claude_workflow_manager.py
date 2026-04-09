import pytest
import httpx
import yaml
from unittest.mock import patch, mock_open, MagicMock
from claude_workflow_manager import load_workflow, execute_task, execute_workflow

def test_load_workflow():
    mock_yaml_content = """tasks:
  - name: task1
    endpoint: https://api.example.com/task1
    parameters:
      key: value1
    api_key: dummy_key1
"""
    with patch('builtins.open', mock_open(read_data=mock_yaml_content)) as mock_file:
        workflow = load_workflow('dummy.yaml')
        assert workflow == {
            'tasks': [
                {
                    'name': 'task1',
                    'endpoint': 'https://api.example.com/task1',
                    'parameters': {'key': 'value1'},
                    'api_key': 'dummy_key1'
                }
            ]
        }
        mock_file.assert_called_once_with('dummy.yaml', 'r')

def test_execute_task_success():
    task = {
        'name': 'test_task',
        'endpoint': 'https://api.example.com/test',
        'parameters': {'key': 'value'},
        'api_key': 'dummy_key'
    }
    with patch('httpx.post') as mock_post:
        mock_response = MagicMock()
        mock_response.json.return_value = {'success': True}
        mock_response.raise_for_status.return_value = None
        mock_post.return_value = mock_response

        result = execute_task(task)
        assert result == {'task': 'test_task', 'result': {'success': True}}

def test_execute_task_failure():
    task = {
        'name': 'test_task',
        'endpoint': 'https://api.example.com/test',
        'parameters': {'key': 'value'},
        'api_key': 'dummy_key'
    }
    with patch('httpx.post') as mock_post:
        mock_post.side_effect = httpx.RequestError("Network error")

        result = execute_task(task)
        assert result == {'task': 'test_task', 'error': 'Network error'}

def test_execute_workflow():
    workflow = {
        'execution_mode': 'sequential',
        'tasks': [
            {
                'name': 'task1',
                'endpoint': 'https://api.example.com/task1',
                'parameters': {'key': 'value1'},
                'api_key': 'dummy_key1'
            },
            {
                'name': 'task2',
                'endpoint': 'https://api.example.com/task2',
                'parameters': {'key': 'value2'},
                'api_key': 'dummy_key2'
            }
        ]
    }
    with patch('claude_workflow_manager.execute_task') as mock_execute_task:
        mock_execute_task.side_effect = lambda task: {'task': task['name'], 'result': 'success'}
        results = execute_workflow(workflow)
        assert results == [
            {'task': 'task1', 'result': 'success'},
            {'task': 'task2', 'result': 'success'}
        ]
