import pytest
from unittest.mock import patch, mock_open
from debugging_ai_assistant import analyze_error, read_file

def test_read_file():
    # Test reading a valid file
    mocked_file = mock_open(read_data="print('Hello, World!')")
    with patch("builtins.open", mocked_file):
        content = read_file("dummy.py")
        assert content == "print('Hello, World!')"

    # Test file not found
    with patch("builtins.open", side_effect=FileNotFoundError):
        content = read_file("nonexistent.py")
        assert content == "Error: File not found."

    # Test other exceptions
    with patch("builtins.open", side_effect=Exception("Unexpected error")):
        content = read_file("error.py")
        assert content == "Error reading file: Unexpected error"

def test_analyze_error():
    # Mock OpenAI API response
    with patch("openai.Completion.create") as mock_openai:
        mock_openai.return_value = type("MockResponse", (object,), {
            "choices": [type("MockChoice", (object,), {"text": "Suggested fix: Check your list indexing."})]
        })

        result = analyze_error("print(my_list[10])", "IndexError: list index out of range")
        assert "Suggested fix" in result

    # Test OpenAI API failure
    with patch("openai.Completion.create", side_effect=Exception("API error")):
        result = analyze_error("print(my_list[10])", "IndexError: list index out of range")
        assert "Error during AI analysis" in result