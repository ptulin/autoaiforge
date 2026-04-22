import pytest
import json
from unittest.mock import patch, Mock
from claude_ui_blueprint_generator import generate_ui_blueprint

def mock_api_response(*args, **kwargs):
    class MockResponse:
        def __init__(self, json_data, status_code):
            self.json_data = json_data
            self.status_code = status_code

        def json(self):
            return self.json_data

        def raise_for_status(self):
            if self.status_code != 200:
                raise requests.RequestException(f"HTTP {self.status_code}")

    if kwargs.get('json', {}).get('description') == "dashboard with sidebar and three cards":
        return MockResponse({"ui": "mock_dashboard"}, 200)
    return MockResponse({}, 400)

@patch('claude_ui_blueprint_generator.requests.post', side_effect=mock_api_response)
def test_generate_ui_blueprint_success(mock_post):
    description = "dashboard with sidebar and three cards"
    output_format = "json"
    result = generate_ui_blueprint(description, output_format)
    assert result == {"ui": "mock_dashboard"}
    mock_post.assert_called_once()

@patch('claude_ui_blueprint_generator.requests.post', side_effect=mock_api_response)
def test_generate_ui_blueprint_invalid_format(mock_post):
    description = "dashboard with sidebar and three cards"
    with pytest.raises(ValueError):
        generate_ui_blueprint(description, "invalid_format")

@patch('claude_ui_blueprint_generator.requests.post', side_effect=mock_api_response)
def test_generate_ui_blueprint_api_error(mock_post):
    description = "invalid description"
    output_format = "json"
    with pytest.raises(RuntimeError):
        generate_ui_blueprint(description, output_format)
    mock_post.assert_called_once()

# Fix: Import requests in the test file to avoid NameError
import requests