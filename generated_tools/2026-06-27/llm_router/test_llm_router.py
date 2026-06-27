import pytest
from unittest.mock import patch, mock_open
import llm_router
import requests

def test_load_config():
    config_data = """
    tasks:
      summarization:
        - endpoint: "http://example.com/summarize"
          api_key: "testkey"
          priority: 1
    """
    with patch("builtins.open", mock_open(read_data=config_data)):
        config = llm_router.load_config("config.yaml")
        assert "tasks" in config
        assert "summarization" in config['tasks']
        assert len(config['tasks']['summarization']) == 1

def test_select_llm():
    config = {
        'tasks': {
            'summarization': [
                {'endpoint': 'http://example.com/summarize', 'api_key': 'testkey', 'priority': 1},
                {'endpoint': 'http://example.com/summarize2', 'api_key': 'testkey2', 'priority': 2}
            ]
        }
    }
    selected = llm_router.select_llm('summarization', config)
    assert selected['endpoint'] == 'http://example.com/summarize'

def test_call_llm():
    with patch('llm_router.requests.post') as mock_post:
        mock_response = mock_post.return_value
        mock_response.status_code = 200
        mock_response.json.return_value = {'output': 'This is a summary.'}

        response = llm_router.call_llm("http://example.com/summarize", "testkey", {"task": "summarization", "input": "Test input"})
        assert response['output'] == 'This is a summary.'

        mock_post.assert_called_once_with(
            "http://example.com/summarize",
            json={"task": "summarization", "input": "Test input"},
            headers={'Authorization': 'Bearer testkey', 'Content-Type': 'application/json'},
            timeout=10
        )

def test_call_llm_connection_error():
    with patch('llm_router.requests.post', side_effect=requests.exceptions.ConnectionError("Connection failed")):
        with pytest.raises(RuntimeError, match="Failed to connect to LLM endpoint"):
            llm_router.call_llm("http://example.com/summarize", "testkey", {"task": "summarization", "input": "Test input"})

def test_select_llm_no_task():
    config = {
        'tasks': {
            'translation': [
                {'endpoint': 'http://example.com/translate', 'api_key': 'testkey', 'priority': 1}
            ]
        }
    }
    with pytest.raises(ValueError, match="Task 'summarization' is not supported"):
        llm_router.select_llm('summarization', config)

def test_select_llm_no_candidates():
    config = {
        'tasks': {
            'summarization': []
        }
    }
    with pytest.raises(ValueError, match="No LLMs configured for task 'summarization'"):
        llm_router.select_llm('summarization', config)
