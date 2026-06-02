import pytest
from unittest.mock import patch
from smart_debugger import debug_error

def test_debug_error_empty_traceback():
    result = debug_error("")
    assert result == {"error": "Empty traceback string provided."}

@patch("openai.ChatCompletion.create")
def test_debug_error_valid_traceback(mock_openai):
    mock_openai.return_value = {
        "choices": [
            {"message": {"content": "This error occurs because you are trying to divide by zero. To fix this, ensure the denominator is not zero."}}
        ]
    }
    traceback_string = "Traceback (most recent call last):\n  File \"example.py\", line 2, in <module>\n    print(1/0)\nZeroDivisionError: division by zero"
    result = debug_error(traceback_string)
    assert "suggestions" in result
    assert "divide by zero" in result["suggestions"].lower()

@patch("openai.ChatCompletion.create")
def test_debug_error_openai_error(mock_openai):
    mock_openai.side_effect = Exception("API error")
    traceback_string = "Traceback (most recent call last):\n  File \"example.py\", line 2, in <module>\n    print(1/0)\nZeroDivisionError: division by zero"
    result = debug_error(traceback_string)
    assert result == {"error": "Unexpected error occurred: API error"}