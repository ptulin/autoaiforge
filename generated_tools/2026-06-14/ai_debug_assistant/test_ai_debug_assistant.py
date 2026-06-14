import pytest
from unittest.mock import patch, MagicMock
from ai_debug_assistant import analyze_error_message

def test_analyze_error_message_success():
    mock_response = MagicMock()
    mock_response.choices = [MagicMock(text="This is a mock suggestion.")]

    with patch("openai.Completion.create", return_value=mock_response):
        with patch("os.getenv", return_value="mock_api_key"):
            result = analyze_error_message("NameError: name 'x' is not defined")
            assert "This is a mock suggestion." in result

def test_analyze_error_message_no_api_key():
    with patch("os.getenv", return_value=None):
        result = analyze_error_message("NameError: name 'x' is not defined")
        assert "OPENAI_API_KEY environment variable is not set." in result

def test_analyze_error_message_api_error():
    with patch("openai.Completion.create", side_effect=Exception("API error")):
        with patch("os.getenv", return_value="mock_api_key"):
            result = analyze_error_message("NameError: name 'x' is not defined")
            assert "An error occurred while processing the error message: API error" in result