import pytest
from unittest.mock import patch, mock_open
from code_sanitizer_ai import analyze_code_with_ai, process_file, process_directory

def test_analyze_code_with_ai():
    mock_response = {
        'choices': [{
            'message': {
                'content': 'Vulnerability found.\n```\nSanitized code here\n```'
            }
        }]
    }

    with patch('openai.ChatCompletion.create', return_value=mock_response):
        analysis, sanitized_code = analyze_code_with_ai("print('Hello World')")
        assert "Vulnerability found." in analysis
        assert sanitized_code == "Sanitized code here"

def test_process_file():
    mock_response = {
        'choices': [{
            'message': {
                'content': 'Vulnerability found.\n```\nSanitized code here\n```'
            }
        }]
    }

    with patch('openai.ChatCompletion.create', return_value=mock_response), \
         patch('os.path.isfile', return_value=True), \
         patch('builtins.open', mock_open(read_data="print('Hello World')")):
        result = process_file('dummy_file.py', sanitize=True)
        assert result == "Sanitized code here"

def test_process_directory():
    mock_response = {
        'choices': [{
            'message': {
                'content': 'Vulnerability found.\n```\nSanitized code here\n```'
            }
        }]
    }

    with patch('openai.ChatCompletion.create', return_value=mock_response), \
         patch('os.path.isdir', return_value=True), \
         patch('os.walk', return_value=[('/dummy_dir', [], ['file1.py'])]), \
         patch('builtins.open', mock_open(read_data="print('Hello World')")):
        results = process_directory('/dummy_dir', sanitize=True)
        assert '/dummy_dir/file1.py' in results
        assert results['/dummy_dir/file1.py'] == "Sanitized code here"
