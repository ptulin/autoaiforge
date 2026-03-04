import pytest
from unittest.mock import patch, MagicMock
from ai_debugger_cli import analyze_with_ai

@patch('ai_debugger_cli.ChatCompletion.create')
def test_analyze_with_ai_success(mock_create):
    mock_response = {
        'choices': [
            {'message': {'content': 'This is a mock response from Claude AI.'}}
        ]
    }
    mock_create.return_value = mock_response

    error_log = "Traceback (most recent call last):\n  File \"example.py\", line 1, in <module>\n    1/0\nZeroDivisionError: division by zero"
    response = analyze_with_ai(error_log)

    assert response == 'This is a mock response from Claude AI.'
    mock_create.assert_called_once()

@patch('ai_debugger_cli.ChatCompletion.create')
def test_analyze_with_ai_empty_input(mock_create):
    mock_response = {
        'choices': [
            {'message': {'content': 'No error log provided.'}}
        ]
    }
    mock_create.return_value = mock_response

    error_log = ""
    response = analyze_with_ai(error_log)

    assert response == 'No error log provided.'
    mock_create.assert_called_once()

@patch('ai_debugger_cli.ChatCompletion.create')
def test_analyze_with_ai_api_error(mock_create):
    mock_create.side_effect = Exception("API Error")

    error_log = "Traceback (most recent call last):\n  File \"example.py\", line 1, in <module>\n    1/0\nZeroDivisionError: division by zero"

    with pytest.raises(Exception, match="API Error"):
        analyze_with_ai(error_log)

    mock_create.assert_called_once()