import pytest
from unittest.mock import patch, mock_open
from ai_bug_finder import analyze_code_with_ai, scan_file, scan_directory

def test_analyze_code_with_ai():
    mock_response = {
        'choices': [
            {
                'message': {
                    'content': "Bug: Missing return statement in function. Suggestion: Add a return statement."
                }
            }
        ]
    }

    with patch('openai.ChatCompletion.create', return_value=mock_response):
        result = analyze_code_with_ai("def example():\n    pass")
        assert "Bug: Missing return statement" in result

def test_scan_file():
    mock_response = {
        'choices': [
            {
                'message': {
                    'content': "Bug: Missing return statement in function. Suggestion: Add a return statement."
                }
            }
        ]
    }

    with patch('openai.ChatCompletion.create', return_value=mock_response):
        with patch('builtins.open', mock_open(read_data="def example():\n    pass")):
            result = scan_file("test_file.py")
            assert result['file'] == "test_file.py"
            assert "Bug: Missing return statement" in result['suggestions']

def test_scan_directory():
    mock_response = {
        'choices': [
            {
                'message': {
                    'content': "Bug: Missing return statement in function. Suggestion: Add a return statement."
                }
            }
        ]
    }

    with patch('openai.ChatCompletion.create', return_value=mock_response):
        with patch('os.walk', return_value=[("/test_dir", ("subdir",), ("file1.py", "file2.py"))]):
            with patch('builtins.open', mock_open(read_data="def example():\n    pass")):
                results = scan_directory("/test_dir")
                assert len(results) == 2
                assert results[0]['file'] == "/test_dir/file1.py"
                assert "Bug: Missing return statement" in results[0]['suggestions']
