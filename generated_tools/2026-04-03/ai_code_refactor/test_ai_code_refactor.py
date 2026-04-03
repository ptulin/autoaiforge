import pytest
from unittest.mock import patch, mock_open
from ai_code_refactor import refactor_code

def test_refactor_code_file_not_found():
    with pytest.raises(FileNotFoundError):
        refactor_code("non_existent_file.py", "output.py", True, True, True)

@patch("builtins.open", new_callable=mock_open, read_data="print('Hello World')")
@patch("openai.Completion.create")
@patch("black.format_str")
def test_refactor_code_success(mock_black, mock_openai, mock_file):
    mock_openai.return_value = {"choices": [{"text": "print('Hello, AI World!')"}]}
    mock_black.return_value = "print('Hello, AI World!')"

    with patch("os.path.exists", return_value=True):
        refactor_code("input.py", "output.py", True, True, True)

    mock_file.assert_called_with("output.py", 'w')
    mock_file().write.assert_called_once_with("print('Hello, AI World!')")

@patch("builtins.open", new_callable=mock_open, read_data="print('Hello World')")
@patch("openai.Completion.create", side_effect=Exception("API error"))
def test_refactor_code_openai_error(mock_openai, mock_file):
    with patch("os.path.exists", return_value=True):
        with pytest.raises(RuntimeError, match="Error communicating with OpenAI API: API error"):
            refactor_code("input.py", "output.py", True, True, True)
