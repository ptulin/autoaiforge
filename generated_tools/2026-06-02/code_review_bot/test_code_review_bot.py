import pytest
import os
from unittest.mock import patch, mock_open
from code_review_bot import process_file, process_directory

def test_process_file_nonexistent():
    result = process_file("nonexistent_file.py")
    assert "does not exist" in result

def test_process_file_read_error():
    with patch("os.path.isfile", return_value=True):
        with patch("builtins.open", side_effect=Exception("Read error")):
            result = process_file("test_file.py")
            assert "Error reading file" in result

@patch("code_review_bot.analyze_code_with_flake8", return_value=["Line 1: Issue 1", "Line 2: Issue 2"])
@patch("code_review_bot.analyze_code_with_openai", return_value="AI feedback")
def test_process_file_success(mock_openai, mock_flake8):
    mock_file_content = "print('Hello, world!')"
    with patch("os.path.isfile", return_value=True):
        with patch("builtins.open", mock_open(read_data=mock_file_content)):
            result = process_file("test_file.py")
            assert "Flake8 Issues:" in result
            assert "Line 1: Issue 1" in result
            assert "OpenAI Feedback:" in result
            assert "AI feedback" in result

@patch("code_review_bot.process_file", return_value="Processed file report")
def test_process_directory(mock_process_file):
    with patch("os.path.isdir", return_value=True):
        with patch("os.walk", return_value=[("/test", [], ["file1.py", "file2.py"])]):
            result = process_directory("/test")
            assert "Processed file report" in result
            assert mock_process_file.call_count == 2
