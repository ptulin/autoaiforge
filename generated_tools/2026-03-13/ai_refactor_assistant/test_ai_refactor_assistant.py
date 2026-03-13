import pytest
from unittest.mock import patch, mock_open
from ai_refactor_assistant import refactor_code_with_ai, format_code_with_black
from pathlib import Path
import openai

def test_refactor_code_with_ai_success():
    mock_response = {
        'choices': [{
            'message': {
                'content': 'def refactored_function():\n    pass'
            }
        }]
    }
    with patch("openai.ChatCompletion.create", return_value=mock_response):
        result = refactor_code_with_ai("fake_api_key", "def test_function():\n    pass")
        assert result == 'def refactored_function():\n    pass'

def test_refactor_code_with_ai_failure():
    with patch("openai.ChatCompletion.create", side_effect=openai.error.OpenAIError("API Error")):
        with pytest.raises(RuntimeError, match="Error while communicating with OpenAI API: API Error"):
            refactor_code_with_ai("fake_api_key", "def test_function():\n    pass")

def test_format_code_with_black():
    with patch("ai_refactor_assistant.Path.exists", return_value=True):
        with patch("ai_refactor_assistant.format_file_in_place") as mock_black:
            mock_black.return_value = None
            try:
                format_code_with_black("test_file.py")
            except RuntimeError:
                pytest.fail("format_code_with_black raised an exception unexpectedly!")

def test_format_code_with_black_invalid_path():
    with patch("ai_refactor_assistant.Path.exists", return_value=False):
        with pytest.raises(RuntimeError, match="Error while formatting code with Black: .*"):
            format_code_with_black("invalid_path")
