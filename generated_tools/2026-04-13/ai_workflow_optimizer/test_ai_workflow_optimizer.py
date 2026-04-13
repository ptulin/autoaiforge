import pytest
import yaml
from unittest.mock import patch, mock_open
from ai_workflow_optimizer import load_workflow_config, execute_task, execute_workflow

@pytest.fixture
def sample_config():
    return {
        'tasks': [
            {'name': 'task1', 'duration': 1},
            {'name': 'task2', 'duration': 2}
        ]
    }

def test_load_workflow_config():
    mock_yaml = """
    tasks:
      - name: task1
        duration: 1
      - name: task2
        duration: 2
    """
    with patch("builtins.open", mock_open(read_data=mock_yaml)):
        config = load_workflow_config("dummy_path.yaml")
        assert config['tasks'][0]['name'] == 'task1'
        assert config['tasks'][1]['duration'] == 2

def test_execute_task():
    task = {'name': 'test_task', 'duration': 1}
    result = execute_task(task)
    assert result['task'] == 'test_task'
    assert result['status'] == 'success'

def test_execute_workflow(sample_config):
    with patch("ai_workflow_optimizer.execute_task", return_value={"task": "mock_task", "status": "success"}):
        results = execute_workflow(sample_config)
        assert len(results) == 2
        assert results[0]['task'] == 'mock_task'
        assert results[0]['status'] == 'success'