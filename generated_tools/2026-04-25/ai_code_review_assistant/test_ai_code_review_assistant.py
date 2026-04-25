import pytest
import json
from unittest.mock import patch, mock_open
from openai.error import OpenAIError
from ai_code_review_assistant import analyze_code_with_ai, load_code_from_file

def test_analyze_code_with_ai_success():
    mock_response = {
        "choices": [
            {
                "message": {
                    "content": "This is a mock review of the code."
                }
            }
        ]
    }
    with patch("ai_code_review_assistant.ChatCompletion.create", return_value=mock_response):
        result = analyze_code_with_ai("fake_api_key", "print('Hello, world!')")
        assert result == "This is a mock review of the code."

def test_analyze_code_with_ai_failure():
    with patch("ai_code_review_assistant.ChatCompletion.create", side_effect=OpenAIError("API Error")):
        result = analyze_code_with_ai("fake_api_key", "print('Hello, world!')")
        assert "Error communicating with OpenAI API" in result

def test_load_code_from_file_success():
    mock_file_content = "print('Hello, world!')"
    with patch("builtins.open", mock_open(read_data=mock_file_content)):
        with patch("os.path.exists", return_value=True):
            result = load_code_from_file("dummy_file.py")
            assert result == mock_file_content

def test_load_code_from_file_not_found():
    with patch("os.path.exists", return_value=False):
        with pytest.raises(FileNotFoundError):
            load_code_from_file("non_existent_file.py")
