import pytest
from unittest.mock import patch, MagicMock
from ai_threat_simulator import simulate_spoof_attack, simulate_brute_force_attack, simulate_data_exfiltration

def mock_requests_get(*args, **kwargs):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.text = "Success"
    return mock_response

def mock_requests_post(*args, **kwargs):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.text = "Success"
    return mock_response

@patch("requests.get", side_effect=mock_requests_get)
def test_simulate_spoof_attack(mock_get):
    logs = simulate_spoof_attack("http://example.com", 3)
    assert len(logs) == 3
    for log in logs:
        assert "spoofed_ip" in log
        assert log["status_code"] == 200
        assert log["response"] == "Success"

@patch("requests.post", side_effect=mock_requests_post)
def test_simulate_brute_force_attack(mock_post):
    logs = simulate_brute_force_attack("http://example.com", 2)
    assert len(logs) == 2
    for log in logs:
        assert "username" in log
        assert "password" in log
        assert log["status_code"] == 200
        assert log["response"] == "Success"

@patch("requests.post", side_effect=mock_requests_post)
def test_simulate_data_exfiltration(mock_post):
    logs = simulate_data_exfiltration("http://example.com", 50)
    assert len(logs) == 1
    assert logs[0]["payload_size"] == 50
    assert logs[0]["status_code"] == 200
    assert logs[0]["response"] == "Success"
