import pytest
from unittest.mock import patch, Mock
from claude_api_tester import send_request, validate_response
import httpx

def test_send_request_success():
    endpoint = "https://api.claude.ai"
    payload = {"key": "value"}
    mock_response = {"result": "success"}

    with patch("httpx.post") as mock_post:
        mock_post.return_value = Mock(status_code=200, json=Mock(return_value=mock_response), raise_for_status=Mock())

        response, response_time = send_request(endpoint, payload)

        assert response == mock_response
        assert response_time is not None

def test_send_request_failure():
    endpoint = "https://api.claude.ai"
    payload = {"key": "value"}

    with patch("httpx.post") as mock_post:
        mock_post.side_effect = httpx.RequestError("Network error", request=Mock())

        response, response_time = send_request(endpoint, payload)

        assert "error" in response
        assert response_time is None

def test_validate_response():
    response = {"result": "success"}
    expected = {"result": "success"}

    assert validate_response(response, expected) is True

    expected = {"result": "failure"}

    assert validate_response(response, expected) is False
