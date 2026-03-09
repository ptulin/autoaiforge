import pytest
from unittest.mock import patch, mock_open
import claude_code_assistant
import argparse

def mock_claude_api(prompt, api_url, api_key):
    return "Mocked Claude AI response."

@patch('claude_code_assistant.call_claude_api', side_effect=mock_claude_api)
def test_process_input(mock_api):
    result = claude_code_assistant.process_input("print('Hello')", "http://mockapi.com", "mockkey", fix=False)
    assert result == "Mocked Claude AI response."

@patch('builtins.open', new_callable=mock_open, read_data="print('Hello')")
@patch('os.path.exists', side_effect=lambda path: path in ['test.py', 'config.yaml'])
def test_main_with_file(mock_exists, mock_open_file):
    with patch('claude_code_assistant.call_claude_api', side_effect=mock_claude_api):
        with patch('argparse.ArgumentParser.parse_args', return_value=argparse.Namespace(file='test.py', text=None, fix=False, output=None, config='config.yaml')):
            with patch('builtins.open', mock_open(read_data="api_url: http://mockapi.com\napi_key: mockkey")) as mock_config_file:
                claude_code_assistant.main()

@patch('os.path.exists', side_effect=lambda path: path == 'config.yaml')
def test_main_missing_file(mock_exists):
    with patch('builtins.print') as mock_print:
        with patch('argparse.ArgumentParser.parse_args', return_value=argparse.Namespace(file='missing.py', text=None, fix=False, output=None, config='config.yaml')):
            with patch('builtins.open', mock_open(read_data="api_url: http://mockapi.com\napi_key: mockkey")):
                claude_code_assistant.main()
                mock_print.assert_called_with("Error: Input file not found.")

@patch('os.path.exists', side_effect=lambda path: path == 'config.yaml')
def test_main_no_input_provided(mock_exists):
    with patch('builtins.print') as mock_print:
        with patch('argparse.ArgumentParser.parse_args', return_value=argparse.Namespace(file=None, text=None, fix=False, output=None, config='config.yaml')):
            with patch('builtins.open', mock_open(read_data="api_url: http://mockapi.com\napi_key: mockkey")):
                claude_code_assistant.main()
                mock_print.assert_called_with("Error: No input provided. Use --file or --text.")