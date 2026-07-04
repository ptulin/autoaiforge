import pytest
from unittest.mock import patch, mock_open
from ai_code_audit import analyze_code_with_openai, analyze_file, analyze_directory

def test_analyze_code_with_openai():
    mock_response = {"choices": [{"text": "Issue 1\nIssue 2"}]}
    with patch("openai.Completion.create", return_value=mock_response):
        result = analyze_code_with_openai("print('Hello, world!')")
        assert result == ["Issue 1", "Issue 2"]

def test_analyze_file():
    mock_response = {"choices": [{"text": "Issue 1\nIssue 2"}]}
    with patch("openai.Completion.create", return_value=mock_response):
        with patch("builtins.open", mock_open(read_data="print('Hello, world!')")):
            result = analyze_file("test.py")
            assert len(result) == 2
            assert result[0][0] == "test.py"
            assert result[0][1] == "INFO"
            assert result[0][2] == "Issue 1"
            assert result[1][0] == "test.py"
            assert result[1][1] == "INFO"
            assert result[1][2] == "Issue 2"

def test_analyze_directory():
    mock_response = {"choices": [{"text": "Issue 1\nIssue 2"}]}
    with patch("openai.Completion.create", return_value=mock_response):
        with patch("os.walk", return_value=[("/path", [], ["file1.py", "file2.py"])]):
            with patch("builtins.open", mock_open(read_data="print('Hello, world!')")):
                result = analyze_directory("/path")
                assert len(result) == 4
                assert result[0][0].endswith("file1.py")
                assert result[0][1] == "INFO"
                assert result[0][2] == "Issue 1"
                assert result[1][0].endswith("file1.py")
                assert result[1][1] == "INFO"
                assert result[1][2] == "Issue 2"
                assert result[2][0].endswith("file2.py")
                assert result[2][1] == "INFO"
                assert result[2][2] == "Issue 1"
                assert result[3][0].endswith("file2.py")
                assert result[3][1] == "INFO"
                assert result[3][2] == "Issue 2"
