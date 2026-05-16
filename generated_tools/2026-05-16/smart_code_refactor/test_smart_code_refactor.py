import pytest
from unittest.mock import patch, mock_open
import smart_code_refactor

def test_refactor_code_file_not_found():
    with pytest.raises(FileNotFoundError):
        smart_code_refactor.refactor_code("non_existent_file.py", "readability")

def test_refactor_code_empty_file():
    with patch("os.path.exists", return_value=True):
        with patch("builtins.open", mock_open(read_data="")):
            with patch("smart_code_refactor.load_api_key", return_value="fake_api_key"):
                with pytest.raises(ValueError):
                    smart_code_refactor.refactor_code("empty_file.py", "readability")

def test_refactor_code_success():
    mock_response = {"choices": [{"text": "refactored code"}]}
    with patch("os.path.exists", return_value=True):
        with patch("builtins.open", mock_open(read_data="original code")):
            with patch("smart_code_refactor.load_api_key", return_value="fake_api_key"):
                with patch("smart_code_refactor.openai.Completion.create", return_value=mock_response):
                    result = smart_code_refactor.refactor_code("file.py", "readability")
                    assert result == "refactored code"

def test_display_diff():
    original = "print(1)"
    refactored = "print(2)"
    diff = smart_code_refactor.display_diff(original, refactored)
    assert "<ins style=\"background:#e6ffe6;\">2</ins>" in diff
    assert "<del style=\"background:#ffe6e6;\">1</del>" in diff
