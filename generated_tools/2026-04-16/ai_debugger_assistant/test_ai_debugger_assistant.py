import pytest
from unittest.mock import patch, mock_open
from ai_debugger_assistant import analyze_traceback

def test_analyze_traceback_file_not_found():
    with pytest.raises(FileNotFoundError):
        analyze_traceback("non_existent_file.py")

@patch("ai_debugger_assistant.openai.ChatCompletion.create")
def test_analyze_traceback_success(mock_openai):
    mock_openai.return_value = {
        'choices': [
            {'message': {'content': "Mocked AI response: Fix the syntax error."}}
        ]
    }
    mock_file_content = "print('Hello World')"
    with patch("builtins.open", mock_open(read_data=mock_file_content)):
        with patch("os.path.exists", return_value=True):
            result = analyze_traceback("example.py")
            assert "Mocked AI response" in result

@patch("ai_debugger_assistant.openai.ChatCompletion.create")
def test_analyze_traceback_ai_error(mock_openai):
    mock_openai.side_effect = Exception("Mocked AI exception")
    mock_file_content = "print('Hello World')"
    with patch("builtins.open", mock_open(read_data=mock_file_content)):
        with patch("os.path.exists", return_value=True):
            result = analyze_traceback("example.py")
            assert "An error occurred while communicating with the AI" in result
