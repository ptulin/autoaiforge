import pytest
from unittest.mock import patch, mock_open
from ai_debug_prompt_generator import parse_error_log, generate_debug_prompt

def test_parse_error_log():
    error_log = "Traceback (most recent call last):\n  File \"example.py\", line 10, in <module>\n    raise ValueError('Invalid value')\nValueError: Invalid value"
    expected_output = {
        "error_type": "ValueError",
        "error_message": "Invalid value",
        "stack_trace": [
            "Traceback (most recent call last):",
            "  File \"example.py\", line 10, in <module>",
            "    raise ValueError('Invalid value')",
            "ValueError: Invalid value"
        ]
    }
    assert parse_error_log(error_log) == expected_output

def test_generate_debug_prompt():
    error_details = {
        "error_type": "ValueError",
        "error_message": "Invalid value",
        "stack_trace": [
            "Traceback (most recent call last):",
            "  File \"example.py\", line 10, in <module>",
            "    raise ValueError('Invalid value')",
            "ValueError: Invalid value"
        ]
    }
    expected_prompt = (
        "I encountered an error in my code. The error type is 'ValueError' "
        "with the message: 'Invalid value'. Here is the stack trace: \n"
        "Traceback (most recent call last):\n"
        "  File \"example.py\", line 10, in <module>\n"
        "    raise ValueError('Invalid value')\n"
        "ValueError: Invalid value\n"
        "Can you help me understand what might be causing this issue and how to resolve it?"
    )
    assert generate_debug_prompt(error_details) == expected_prompt

def test_main_file_not_found():
    with patch('builtins.open', mock_open()) as mocked_open:
        mocked_open.side_effect = FileNotFoundError("File not found")
        with pytest.raises(FileNotFoundError):
            mocked_open("non_existent_file.txt", 'r')