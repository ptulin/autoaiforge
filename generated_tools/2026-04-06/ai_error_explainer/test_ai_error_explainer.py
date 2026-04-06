import pytest
from unittest.mock import patch, MagicMock
from ai_error_explainer import explain_error
import openai

def test_explain_error_success():
    mock_response = {
        'choices': [
            {
                'message': {
                    'content': 'This is a mock explanation for the error.'
                }
            }
        ]
    }

    with patch('openai.ChatCompletion.create', return_value=mock_response):
        result = explain_error("fake_api_key", "TypeError: unsupported operand type(s) for +: 'int' and 'str'")
        assert "explanation" in result
        assert result["explanation"] == "This is a mock explanation for the error."

def test_explain_error_api_error():
    with patch('openai.ChatCompletion.create', side_effect=openai.error.OpenAIError("API error")):
        result = explain_error("fake_api_key", "Some error message")
        assert "error" in result
        assert "Failed to retrieve explanation" in result["error"]

def test_explain_error_empty_message():
    with patch('openai.ChatCompletion.create') as mock_create:
        result = explain_error("fake_api_key", "")
        mock_create.assert_not_called()
        assert "error" in result
        assert result["error"] == "Error message is empty."
