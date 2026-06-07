import pytest
from unittest.mock import patch, mock_open
from ai_code_vuln_scanner import scan_file, scan_directory

def fake_ai_model(code):
    """Mock AI model that returns fake vulnerabilities."""
    return [
        {'line': 1, 'issue': 'Hardcoded secret', 'suggestion': 'Use environment variables instead.'},
        {'line': 5, 'issue': 'Insecure function usage', 'suggestion': 'Use a secure alternative.'}
    ]

def test_scan_file():
    mock_code = """password = '12345'\nos.system('rm -rf /')"""
    with patch("builtins.open", mock_open(read_data=mock_code)):
        vulnerabilities = scan_file("test_file.py", fake_ai_model)
        assert len(vulnerabilities) == 2
        assert vulnerabilities[0]['line'] == 1
        assert vulnerabilities[1]['line'] == 5

def test_scan_file_error():
    with patch("builtins.open", side_effect=FileNotFoundError):
        vulnerabilities = scan_file("non_existent_file.py", fake_ai_model)
        assert len(vulnerabilities) == 1
        assert vulnerabilities[0]['issue'].startswith("Error reading file")

def test_scan_directory():
    mock_code = """password = '12345'\nos.system('rm -rf /')"""
    with patch("os.walk") as mock_walk, patch("builtins.open", mock_open(read_data=mock_code)):
        mock_walk.return_value = [
            ("/test_dir", ("subdir",), ("file1.py", "file2.py"))
        ]
        results = scan_directory("/test_dir", fake_ai_model)
        assert len(results) == 2
        assert "/test_dir/file1.py" in results
        assert "/test_dir/file2.py" in results
        assert len(results["/test_dir/file1.py"]) == 2
        assert len(results["/test_dir/file2.py"]) == 2