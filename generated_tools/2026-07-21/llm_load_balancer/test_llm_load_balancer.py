import pytest
from unittest.mock import patch, MagicMock
from llm_load_balancer import LLMRouter, LLMInstance, requests

@pytest.fixture
def mock_router():
    router = LLMRouter()
    router.add_instance("local1", "http://localhost:5001/query", 2)
    router.add_instance("cloud", "https://cloud-llm.example.com/query", 5)
    return router

@patch('llm_load_balancer.requests.post')
def test_route_request_success(mock_post, mock_router):
    mock_post.return_value = MagicMock(status_code=200, json=lambda: {"response": "Success"})
    response = mock_router.route_request("Test query")
    assert response == {"response": "Success"}

@patch('llm_load_balancer.requests.post')
def test_route_request_all_instances_fail(mock_post, mock_router):
    mock_post.side_effect = requests.RequestException("Network error")
    response = mock_router.route_request("Test query")
    assert response == {"error": "All instances failed"}

@patch('llm_load_balancer.requests.post')
def test_route_request_quota_exceeded(mock_post, mock_router):
    mock_post.return_value = MagicMock(status_code=200, json=lambda: {"response": "Success"})
    mock_router.instances[0].requests_handled = 2  # Simulate quota exceeded for local1
    response = mock_router.route_request("Test query")
    assert response == {"response": "Success"}
    assert mock_router.instances[1].requests_handled == 1  # Ensure cloud instance was used