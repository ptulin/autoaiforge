import pytest
import yaml
from unittest.mock import patch, MagicMock
from ai_workflow_orchestrator import WorkflowOrchestrator, load_workflow

def test_load_workflow(tmp_path):
    workflow_content = """
    step1:
      type: api_call
      url: http://example.com/api
    """
    workflow_file = tmp_path / "workflow.yaml"
    workflow_file.write_text(workflow_content)

    workflow = load_workflow(workflow_file)
    assert 'step1' in workflow
    assert workflow['step1']['type'] == 'api_call'

def test_execute_step_api_call():
    step = {
        'type': 'api_call',
        'url': 'http://example.com/api',
        'payload': {'key': 'value'}
    }

    orchestrator = WorkflowOrchestrator({})

    with patch('requests.post') as mock_post:
        mock_response = MagicMock()
        mock_response.json.return_value = {'result': 'success'}
        mock_response.raise_for_status = MagicMock()
        mock_post.return_value = mock_response

        result = orchestrator.execute_step(step)
        assert result == {'result': 'success'}
        mock_post.assert_called_once_with('http://example.com/api', json={'key': 'value'}, headers={})

def test_run_workflow():
    workflow = {
        'step1': {
            'type': 'api_call',
            'url': 'http://example.com/api',
            'payload': {'key': 'value'}
        }
    }

    orchestrator = WorkflowOrchestrator(workflow)

    with patch('requests.post') as mock_post:
        mock_response = MagicMock()
        mock_response.json.return_value = {'result': 'success'}
        mock_response.raise_for_status = MagicMock()
        mock_post.return_value = mock_response

        results = orchestrator.run()
        assert 'step1' in results
        assert results['step1'] == {'result': 'success'}