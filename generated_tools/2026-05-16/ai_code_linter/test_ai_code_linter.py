import pytest
from unittest.mock import patch, mock_open
import openai
from ai_code_linter import lint_code

def test_lint_code_file_not_found():
    with pytest.raises(FileNotFoundError):
        lint_code("non_existent_file.py")

def test_lint_code_empty_file():
    with patch("os.path.exists", return_value=True):
        with patch("builtins.open", mock_open(read_data="")):
            result = lint_code("empty_file.py")
            assert result == "The file is empty. No code to lint."

def test_lint_code_valid_file():
    mock_response = {"choices": [{"text": "Suggestion: Use better variable names."}]}
    with patch("os.path.exists", return_value=True):
        with patch("builtins.open", mock_open(read_data="x = 1")):
            with patch("openai.Completion.create", return_value=mock_response):
                result = lint_code("valid_file.py")
                assert result == "Suggestion: Use better variable names."

def test_lint_code_no_suggestions():
    mock_response = {"choices": []}
    with patch("os.path.exists", return_value=True):
        with patch("builtins.open", mock_open(read_data="x = 1")):
            with patch("openai.Completion.create", return_value=mock_response):
                result = lint_code("valid_file.py")
                assert result == "No suggestions returned by the AI."

def test_lint_code_api_error():
    with patch("os.path.exists", return_value=True):
        with patch("builtins.open", mock_open(read_data="x = 1")):
            with patch("openai.Completion.create", side_effect=openai.error.OpenAIError("API error")):
                result = lint_code("valid_file.py")
                assert result == "Error while communicating with OpenAI API: API error"
