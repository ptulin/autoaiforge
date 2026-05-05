import pytest
from unittest.mock import patch, Mock
import task_chain_orchestrator
import requests

@pytest.fixture
def mock_api_response():
    return {"response": "Mocked AI response"}

def test_call_ai_api_success(mock_api_response):
    with patch('requests.post') as mock_post:
        mock_post.return_value = Mock(status_code=200, json=lambda: mock_api_response)
        result = task_chain_orchestrator.call_ai_api("http://mockapi.com", "mock_key", "Test prompt")
        assert result == mock_api_response

def test_call_ai_api_failure():
    with patch('requests.post') as mock_post:
        mock_post.side_effect = requests.exceptions.RequestException("API error")
        result = task_chain_orchestrator.call_ai_api("http://mockapi.com", "mock_key", "Test prompt")
        assert "error" in result

def test_execute_task_chain(mock_api_response):
    config = {
        "tasks": [
            {"type": "sequential", "prompt": "Task 1"},
            {"type": "conditional", "prompt": "Task 2", "condition": "True"}
        ]
    }
    with patch('task_chain_orchestrator.call_ai_api', return_value=mock_api_response):
        results = task_chain_orchestrator.execute_task_chain(config, "http://mockapi.com", "mock_key")
        assert len(results) == 2
        assert results[0] == mock_api_response
        assert results[1] == mock_api_response
