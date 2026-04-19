import pytest
from unittest.mock import patch, mock_open
from claude_code_assist import process_code

def test_process_code_file_not_found():
    result = process_code("non_existent_file.py", "debug", "fake_api_key")
    assert result is None

@patch("claude_code_assist.get_claude_response")
def test_process_code_debug(mock_get_claude_response):
    mock_get_claude_response.return_value = "Debugged code"
    with patch("os.path.isfile", return_value=True):
        with patch("builtins.open", mock_open(read_data="print('Hello, World!')")):
            result = process_code("example.py", "debug", "fake_api_key")
    assert result == "Debugged code"
    mock_get_claude_response.assert_called_once_with("Perform the following action on the code: debug\n\nCode:\nprint('Hello, World!')", "fake_api_key")

@patch("claude_code_assist.get_claude_response")
def test_process_code_suggest(mock_get_claude_response):
    mock_get_claude_response.return_value = "Suggested code"
    with patch("os.path.isfile", return_value=True):
        with patch("builtins.open", mock_open(read_data="def add(a, b):\n    pass")):
            result = process_code("example.py", "suggest", "fake_api_key")
    assert result == "Suggested code"
    mock_get_claude_response.assert_called_once_with("Perform the following action on the code: suggest\n\nCode:\ndef add(a, b):\n    pass", "fake_api_key")