import pytest
from unittest.mock import patch, MagicMock
from openai import OpenAIError
from ai_debugger_assist import analyze_stack_trace

def test_analyze_stack_trace_success():
    mock_response = {
        'choices': [{
            'message': {
                'content': 'This is a mock debugging suggestion.'
            }
        }]
    }

    with patch('ai_debugger_assist.ChatCompletion.create', return_value=mock_response):
        trace = 'Traceback (most recent call last):\n  File "example.py", line 1, in <module>\n    1 / 0\nZeroDivisionError: division by zero'
        result = analyze_stack_trace(trace)
        assert result == 'This is a mock debugging suggestion.'

def test_analyze_stack_trace_openai_error():
    with patch('ai_debugger_assist.ChatCompletion.create', side_effect=OpenAIError("API Error")):
        trace = 'Traceback (most recent call last):\n  File "example.py", line 1, in <module>\n    1 / 0\nZeroDivisionError: division by zero'
        with pytest.raises(OpenAIError, match="Failed to analyze stack trace: API Error"):
            analyze_stack_trace(trace)

def test_analyze_stack_trace_empty_trace():
    with patch('ai_debugger_assist.ChatCompletion.create') as mock_create:
        trace = ''
        with pytest.raises(ValueError, match="Empty stack trace provided."):
            analyze_stack_trace(trace)
        mock_create.assert_not_called()
