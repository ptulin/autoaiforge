import pytest
from unittest.mock import patch, MagicMock
from ai_api_monitor import ProxyServer, ProxyHTTPRequestHandler
import json

@pytest.fixture
def mock_server():
    server = ProxyServer(('localhost', 0), ProxyHTTPRequestHandler, "test_log.json", "http://mockapi.com")
    yield server

@patch("httpx.post")
def test_forward_request(mock_post, mock_server):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.text = "{}"
    mock_response.headers = {}
    mock_post.return_value = mock_response

    response = mock_server.forward_request("/test", b"{}", {"Content-Type": "application/json"})
    assert response.status_code == 200
    assert response.text == "{}"

@patch("httpx.post")
def test_log_request(mock_post, mock_server):
    mock_server.log_request("/test", b"password=1234", {"Content-Type": "application/json"})
    assert len(mock_server.logs) == 1
    assert "anomaly" in mock_server.logs[0]
    assert mock_server.logs[0]["anomaly"] == "Sensitive information detected"

@patch("httpx.post")
def test_save_logs(mock_post, mock_server):
    mock_server.log_request("/test", b"password=1234", {"Content-Type": "application/json"})
    mock_server.save_logs()
    with open("test_log.json") as f:
        logs = json.load(f)
    assert len(logs) == 1
    assert logs[0]["type"] == "request"
