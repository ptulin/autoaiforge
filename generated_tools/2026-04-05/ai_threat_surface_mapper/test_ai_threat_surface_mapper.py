import pytest
from unittest.mock import patch, mock_open
from ai_threat_surface_mapper import scan_file, scan_directory

def test_scan_file_hardcoded_key():
    mock_content = "api_key = '12345'"
    with patch("builtins.open", mock_open(read_data=mock_content)):
        result = scan_file("dummy_path.py")
    assert "Hardcoded API key or secret detected." in result

def test_scan_file_insecure_http():
    mock_content = "url = 'http://example.com'"
    with patch("builtins.open", mock_open(read_data=mock_content)):
        result = scan_file("dummy_path.py")
    assert "Insecure HTTP usage detected." in result

def test_scan_file_weak_encryption():
    mock_content = "hash = md5(password.encode())"
    with patch("builtins.open", mock_open(read_data=mock_content)):
        result = scan_file("dummy_path.py")
    assert "Weak encryption (MD5) detected." in result

def test_scan_directory():
    with patch("os.walk") as mock_walk:
        mock_walk.return_value = [
            ("/test", ("subdir",), ("file1.py", "file2.yaml")),
        ]
        with patch("builtins.open", mock_open(read_data="api_key = '12345'")):
            results = scan_directory("/test")
    assert "/test/file1.py" in results
    assert "Hardcoded API key or secret detected." in results["/test/file1.py"]
    assert "/test/file2.yaml" in results
    assert "Hardcoded API key or secret detected." in results["/test/file2.yaml"]