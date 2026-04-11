import pytest
import openai
from unittest.mock import patch, MagicMock
from ai_refactor_assistant import refactor_code

def test_refactor_code_valid_input():
    input_code = "def add(a, b):\n    return a + b"
    mock_response = {
        "choices": [
            {"message": {"content": "def add(a, b):\n    return a + b\n"}}
        ]
    }
    with patch("openai.ChatCompletion.create", return_value=mock_response):
        refactored_code = refactor_code(input_code, openai_api_key="fake_api_key")
        assert "def add(a, b):" in refactored_code


def test_refactor_code_invalid_syntax():
    input_code = "def add(a, b):\nreturn a + b"
    with pytest.raises(ValueError, match="Invalid Python code provided"):
        refactor_code(input_code, openai_api_key="fake_api_key")

def test_refactor_code_openai_error():
    input_code = "def add(a, b):\n    return a + b"
    with patch("openai.ChatCompletion.create", side_effect=openai.error.OpenAIError("API error")):
        with pytest.raises(RuntimeError, match="Error communicating with OpenAI API"):
            refactor_code(input_code, openai_api_key="fake_api_key")
