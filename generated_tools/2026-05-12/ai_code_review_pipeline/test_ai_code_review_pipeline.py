import pytest
import json
from unittest.mock import patch
from ai_code_review_pipeline import fetch_ai_feedback, aggregate_feedback, filter_feedback

def test_fetch_ai_feedback():
    mock_response = {"feedback": "Looks good!"}
    with patch("requests.post") as mock_post:
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = mock_response

        result = fetch_ai_feedback("http://mockapi.com/review", "mock_api_key", "print('Hello World')")
        assert result == mock_response

def test_aggregate_feedback():
    feedback_list = [
        {"style": "Use consistent naming conventions."},
        {"performance": "Consider optimizing this loop."},
        {"style": "Avoid using global variables."}
    ]
    aggregated = aggregate_feedback(feedback_list)
    assert aggregated == {
        "style": ["Use consistent naming conventions.", "Avoid using global variables."],
        "performance": ["Consider optimizing this loop."]
    }

def test_filter_feedback():
    aggregated_feedback = {
        "style": ["Use consistent naming conventions."],
        "performance": ["Consider optimizing this loop."],
        "security": ["Avoid using hardcoded secrets."]
    }
    filters = ["style", "security"]
    filtered = filter_feedback(aggregated_feedback, filters)
    assert filtered == {
        "style": ["Use consistent naming conventions."],
        "security": ["Avoid using hardcoded secrets."]
    }