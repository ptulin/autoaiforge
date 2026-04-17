import pytest
from unittest.mock import patch
from code_suggestion_compare import fetch_code_suggestion, compare_suggestions
import requests

def mock_post(*args, **kwargs):
    class MockResponse:
        def __init__(self, json_data, status_code):
            self.json_data = json_data
            self.status_code = status_code

        def json(self):
            return self.json_data

        def raise_for_status(self):
            if self.status_code != 200:
                raise requests.exceptions.HTTPError(f"HTTP {self.status_code}")

    if "valid_api_key_1" in kwargs["headers"]["Authorization"]:
        return MockResponse({"code": "def add(a, b):\n    return a + b"}, 200)
    elif "valid_api_key_2" in kwargs["headers"]["Authorization"]:
        return MockResponse({"code": "def add(a, b):\n    return b + a"}, 200)
    else:
        return MockResponse({}, 403)

@patch("requests.post", side_effect=mock_post)
def test_fetch_code_suggestion(mock_post):
    result = fetch_code_suggestion("valid_api_key_1", "def add(a, b): ...")
    assert result == "def add(a, b):\n    return a + b"

    result = fetch_code_suggestion("invalid_api_key", "def add(a, b): ...")
    assert "Error fetching suggestion" in result

@patch("requests.post", side_effect=mock_post)
def test_compare_suggestions(mock_post):
    api_keys = ["valid_api_key_1", "valid_api_key_2"]
    prompt = "def add(a, b): ..."

    result = compare_suggestions(api_keys, prompt)

    assert "model_1" in result["suggestions"]
    assert "model_2" in result["suggestions"]
    assert result["suggestions"]["model_1"] == "def add(a, b):\n    return a + b"
    assert result["suggestions"]["model_2"] == "def add(a, b):\n    return b + a"
    assert "model_1_vs_model_2" in result["diffs"]
    assert "-    return a + b" in result["diffs"]["model_1_vs_model_2"]
    assert "+    return b + a" in result["diffs"]["model_1_vs_model_2"]

@patch("requests.post", side_effect=mock_post)
def test_compare_suggestions_with_empty_api_keys(mock_post):
    api_keys = []
    prompt = "def add(a, b): ..."

    result = compare_suggestions(api_keys, prompt)

    assert result["suggestions"] == {}
    assert result["diffs"] == {}
