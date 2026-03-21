import pytest
import yaml
from unittest.mock import patch, MagicMock
from ai_workflow_builder import execute_ai_task, execute_workflow

def test_execute_ai_task():
    with patch('openai.Completion.create') as mock_create:
        mock_create.return_value = MagicMock(choices=[MagicMock(text='Test response')])
        task = {
            'prompt': 'Test prompt',
            'model': 'text-davinci-003',
            'max_tokens': 50
        }
        result = execute_ai_task(task)
        assert result == 'Test response'
        mock_create.assert_called_once()

def test_execute_workflow():
    with patch('ai_workflow_builder.execute_ai_task') as mock_execute_ai_task:
        mock_execute_ai_task.return_value = 'Mocked AI response'
        config = {
            'workflow': [
                {'type': 'ai_task', 'name': 'Step 1', 'prompt': 'Test prompt', 'model': 'text-davinci-003'}
            ]
        }
        results = execute_workflow(config)
        assert len(results) == 1
        assert results[0]['result'] == 'Mocked AI response'
        mock_execute_ai_task.assert_called_once()

def test_execute_workflow_unsupported_task():
    config = {
        'workflow': [
            {'type': 'unsupported_task', 'name': 'Step 1'}
        ]
    }
    results = execute_workflow(config)
    assert len(results) == 1
    assert results[0]['error'] == 'Unsupported task type'
