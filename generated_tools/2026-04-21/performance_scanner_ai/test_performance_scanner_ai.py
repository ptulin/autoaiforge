import pytest
from unittest.mock import patch, mock_open
from performance_scanner_ai import analyze_code, scan_code

def test_analyze_code():
    mock_response = {
        'choices': [
            {
                'message': {
                    'content': "This code has a performance bottleneck in the nested loops. Consider optimizing by using vectorized operations."
                }
            }
        ]
    }

    with patch('performance_scanner_ai.ChatCompletion.create', return_value=mock_response):
        code = "for i in range(100):\n    for j in range(100):\n        print(i, j)"
        result = analyze_code(code)
        assert "analysis" in result
        assert "bottleneck" in result["analysis"]

def test_scan_code_file_not_found():
    result = scan_code("non_existent_file.py")
    assert "error" in result
    assert result["error"] == "File not found."

def test_scan_code_success():
    mock_response = {
        'choices': [
            {
                'message': {
                    'content': "This code has a performance bottleneck in the nested loops. Consider optimizing by using vectorized operations."
                }
            }
        ]
    }

    with patch('performance_scanner_ai.ChatCompletion.create', return_value=mock_response):
        with patch("os.path.isfile", return_value=True):
            with patch("builtins.open", mock_open(read_data="for i in range(100):\n    for j in range(100):\n        print(i, j)")):
                result = scan_code("dummy_path.py")
                assert "analysis" in result
                assert "bottleneck" in result["analysis"]