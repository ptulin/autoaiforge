import pytest
from unittest.mock import patch, mock_open
from code_refactor_ai import analyze_and_refactor_code, process_directory

def test_analyze_and_refactor_code():
    mock_response = {
        'choices': [{
            'message': {
                'content': "Refactored code content"
            }
        }]
    }

    with patch('openai.ChatCompletion.create', return_value=mock_response):
        with patch('builtins.open', mock_open(read_data="original code")):
            result = analyze_and_refactor_code("test.py", apply_changes=False)
            assert result == "Refactored code content"

def test_analyze_and_refactor_code_apply():
    mock_response = {
        'choices': [{
            'message': {
                'content': "Refactored code content"
            }
        }]
    }

    with patch('openai.ChatCompletion.create', return_value=mock_response):
        with patch('builtins.open', mock_open(read_data="original code")) as mocked_file:
            result = analyze_and_refactor_code("test.py", apply_changes=True)
            mocked_file().write.assert_called_once_with("Refactored code content")
            assert result == "Changes applied successfully."

def test_process_directory():
    mock_response = {
        'choices': [{
            'message': {
                'content': "Refactored code content"
            }
        }]
    }

    with patch('openai.ChatCompletion.create', return_value=mock_response):
        with patch('os.walk', return_value=[("/test_dir", [], ["file1.py", "file2.py"])]):
            with patch('builtins.open', mock_open(read_data="original code")):
                results = process_directory("/test_dir", apply_changes=False)
                assert results == {
                    "/test_dir/file1.py": "Refactored code content",
                    "/test_dir/file2.py": "Refactored code content"
                }