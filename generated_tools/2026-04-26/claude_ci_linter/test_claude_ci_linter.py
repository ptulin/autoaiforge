import pytest
import unittest.mock as mock
from claude_ci_linter import get_staged_files, analyze_code_with_claude, run_linter

def test_get_staged_files():
    with mock.patch("subprocess.run") as mock_run:
        mock_run.return_value.stdout = "file1.py\nfile2.py\nfile3.txt\n"
        mock_run.return_value.returncode = 0
        files = get_staged_files()
        assert files == ["file1.py", "file2.py"]

def test_analyze_code_with_claude():
    mock_response = {
        "choices": [{"message": {"content": "This is a test feedback."}}]
    }
    with mock.patch("openai.ChatCompletion.create", return_value=mock_response):
        feedback = analyze_code_with_claude("print('Hello, World!')", "fake_api_key")
        assert feedback == "This is a test feedback."

def test_run_linter():
    with mock.patch("claude_ci_linter.get_staged_files", return_value=["file1.py"]):
        with mock.patch("builtins.open", mock.mock_open(read_data="print('Hello, World!')")):
            with mock.patch("claude_ci_linter.analyze_code_with_claude", return_value="Test feedback") as mock_analyze:
                run_linter("fake_api_key")
                mock_analyze.assert_called_once_with("print('Hello, World!')", "fake_api_key")
