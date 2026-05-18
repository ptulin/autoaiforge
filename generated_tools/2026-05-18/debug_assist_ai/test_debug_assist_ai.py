import pytest
from unittest.mock import patch, MagicMock
import openai
from debug_assist_ai import analyze_error_message

def test_analyze_error_message_success():
    mock_response = MagicMock()
    mock_response.choices = [MagicMock(text="Mocked suggestion for fixing the error.")]

    with patch('openai.Completion.create', return_value=mock_response):
        result = analyze_error_message("IndexError: list index out of range")
        assert result == "Mocked suggestion for fixing the error."

def test_analyze_error_message_api_error():
    with patch('openai.Completion.create', side_effect=openai.error.OpenAIError("API error")):
        result = analyze_error_message("IndexError: list index out of range")
        assert result == "Error communicating with OpenAI API: API error"

def test_analyze_error_message_empty_input():
    mock_response = MagicMock()
    mock_response.choices = [MagicMock(text="Mocked suggestion for empty input.")]

    with patch('openai.Completion.create', return_value=mock_response) as mock_create:
        result = analyze_error_message("")
        mock_create.assert_called_once()
        assert "Analyze the following Python error message or stack trace" in mock_create.call_args[1]['prompt']
        assert result == "Mocked suggestion for empty input."

def test_analyze_error_message_unexpected_error():
    with patch('openai.Completion.create', side_effect=Exception("Unexpected error")):
        result = analyze_error_message("Some error")
        assert result == "An unexpected error occurred: Unexpected error"