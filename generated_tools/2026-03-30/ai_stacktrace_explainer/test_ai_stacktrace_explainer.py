import pytest
from unittest.mock import patch, mock_open
from ai_stacktrace_explainer import read_stack_trace, explain_stack_trace

def test_read_stack_trace_file_not_found():
    with pytest.raises(FileNotFoundError):
        read_stack_trace("non_existent_file.txt")

def test_read_stack_trace_success():
    mock_content = "Traceback (most recent call last):\n  File \"<stdin>\", line 1, in <module>\nZeroDivisionError: division by zero"
    with patch("builtins.open", mock_open(read_data=mock_content)):
        with patch("os.path.exists", return_value=True):
            result = read_stack_trace("mock_file.txt")
            assert result == mock_content

def test_explain_stack_trace():
    mock_response = {
        'choices': [
            {
                'message': {
                    'content': 'This is a mock explanation of the stack trace.'
                }
            }
        ]
    }
    with patch("ai_stacktrace_explainer.ChatCompletion.create", return_value=mock_response):
        with patch("ai_stacktrace_explainer.os.getenv", return_value="mock_api_key"):
            stack_trace = "Traceback (most recent call last):\n  File \"<stdin>\", line 1, in <module>\nZeroDivisionError: division by zero"
            explanation = explain_stack_trace(stack_trace)
            assert explanation == "This is a mock explanation of the stack trace."
