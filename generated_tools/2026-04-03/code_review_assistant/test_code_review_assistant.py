import pytest
from unittest.mock import patch, mock_open
from code_review_assistant import analyze_code, process_file, process_directory

def test_analyze_code():
    mock_response = {
        "choices": [{"message": {"content": "This is a mock review."}}]
    }
    with patch("openai.ChatCompletion.create", return_value=mock_response):
        result = analyze_code("print('Hello, World!')")
        assert result == "This is a mock review."

def test_process_file():
    mock_response = {
        "choices": [{"message": {"content": "This is a mock review for file."}}]
    }
    with patch("openai.ChatCompletion.create", return_value=mock_response):
        with patch("builtins.open", mock_open(read_data="print('Hello, World!')")):
            result = process_file("test_file.py", "gpt-3.5-turbo", None)
            assert result == "This is a mock review for file."

def test_process_directory():
    mock_response = {
        "choices": [{"message": {"content": "This is a mock review for file."}}]
    }
    with patch("openai.ChatCompletion.create", return_value=mock_response):
        with patch("os.walk", return_value=[("/test_dir", ("subdir",), ("file1.py", "file2.py"))]):
            with patch("builtins.open", mock_open(read_data="print('Hello, World!')")):
                result = process_directory("/test_dir", "gpt-3.5-turbo", None)
                assert len(result) == 2
                assert result["/test_dir/file1.py"] == "This is a mock review for file."
                assert result["/test_dir/file2.py"] == "This is a mock review for file."
