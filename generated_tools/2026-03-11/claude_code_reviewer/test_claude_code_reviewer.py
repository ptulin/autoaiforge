import pytest
from unittest.mock import patch, mock_open
from claude_code_reviewer import analyze_code, process_path
import requests

def test_analyze_code_file_not_found():
    result = analyze_code("nonexistent_file.py", "http://fakeapi.com")
    assert "error" in result
    assert "File not found" in result["error"]

@patch("builtins.open", new_callable=mock_open, read_data="print('Hello, World!')")
@patch("requests.post")
def test_analyze_code_success(mock_post, mock_file):
    mock_post.return_value.status_code = 200
    mock_post.return_value.json.return_value = {"feedback": "Looks good!"}

    result = analyze_code("test_file.py", "http://fakeapi.com")
    assert "feedback" in result
    assert result["feedback"] == "Looks good!"

@patch("builtins.open", new_callable=mock_open, read_data="print('Hello, World!')")
@patch("requests.post")
def test_analyze_code_network_error(mock_post, mock_file):
    mock_post.side_effect = requests.exceptions.RequestException("Network error")

    result = analyze_code("test_file.py", "http://fakeapi.com")
    assert "error" in result
    assert "Network error" in result["error"]

@patch("claude_code_reviewer.analyze_code")
def test_process_path_directory(mock_analyze_code, tmp_path):
    mock_analyze_code.return_value = {"feedback": "Looks good!"}

    # Create temporary Python files
    file1 = tmp_path / "file1.py"
    file1.write_text("print('File 1')")
    file2 = tmp_path / "file2.py"
    file2.write_text("print('File 2')")

    result = process_path(tmp_path, "http://fakeapi.com")

    assert len(result) == 2
    assert "file1.py" in result
    assert "file2.py" in result
    assert result["file1.py"] == {"feedback": "Looks good!"}
    assert result["file2.py"] == {"feedback": "Looks good!"}