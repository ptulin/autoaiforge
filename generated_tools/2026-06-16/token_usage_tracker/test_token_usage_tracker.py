import pytest
from unittest.mock import patch, MagicMock
from token_usage_tracker import TokenUsageTracker

@pytest.fixture
def mock_response():
    return {
        "usage": {
            "total_tokens": 10
        }
    }

@patch("token_usage_tracker.requests.post")
def test_make_request(mock_post, mock_response):
    mock_post.return_value = MagicMock(status_code=200, json=lambda: mock_response)

    tracker = TokenUsageTracker(api_key="test_key", model="gpt-4")
    response = tracker.make_request("Test prompt")

    assert response == mock_response
    assert len(tracker.usage_log) == 1
    assert tracker.usage_log[0]["tokens_used"] == 10

@patch("token_usage_tracker.requests.post")
def test_make_request_error(mock_post):
    import requests  # Ensure requests is imported for the test
    mock_post.side_effect = requests.exceptions.RequestException("API error")

    tracker = TokenUsageTracker(api_key="test_key", model="gpt-4")
    response = tracker.make_request("Test prompt")

    assert response is None
    assert len(tracker.usage_log) == 0

def test_generate_report():
    tracker = TokenUsageTracker(api_key="test_key", model="gpt-4")
    tracker.usage_log = [
        {"prompt": "Test 1", "tokens_used": 10},
        {"prompt": "Test 2", "tokens_used": 20}
    ]

    report = tracker.generate_report("text")
    assert "Test 1" in report
    assert "Test 2" in report
    assert "30" in report

    csv_report = tracker.generate_report("csv")
    assert "Test 1" in csv_report
    assert "Test 2" in csv_report
    assert "30" in csv_report