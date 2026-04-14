import pytest
import os
from unittest.mock import mock_open, patch
from ai_integration_scanner import scan_file, scan_directory

def test_scan_file_hardcoded_api_key():
    mock_code = """
    api_key = "sk-1234567890abcdef1234567890abcdef"
    """
    with patch("builtins.open", mock_open(read_data=mock_code)):
        issues = scan_file("mock_file.py")
        assert len(issues) == 1
        assert issues[0]['issue'] == 'Hardcoded API key detected.'

def test_scan_file_http_request():
    mock_code = """
    response = requests.get("http://example.com")
    """
    with patch("builtins.open", mock_open(read_data=mock_code)):
        issues = scan_file("mock_file.py")
        assert len(issues) == 1
        assert issues[0]['issue'] == 'Unencrypted HTTP request detected.'

def test_scan_file_unsafe_eval():
    mock_code = """
    result = eval("2 + 2")
    """
    with patch("builtins.open", mock_open(read_data=mock_code)):
        issues = scan_file("mock_file.py")
        assert len(issues) == 1
        assert issues[0]['issue'] == 'Usage of unsafe function eval detected.'

def test_scan_directory():
    mock_code = """
    api_key = "sk-1234567890abcdef1234567890abcdef"
    """
    with patch("os.walk") as mock_walk, patch("builtins.open", mock_open(read_data=mock_code)):
        mock_walk.return_value = [("/mock_dir", ("subdir",), ["file1.py"])]
        issues = scan_directory("/mock_dir")
        assert len(issues) == 1
        assert issues[0]['file'] == "/mock_dir/file1.py"
        assert issues[0]['issue'] == 'Hardcoded API key detected.'