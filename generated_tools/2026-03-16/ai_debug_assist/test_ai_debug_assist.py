import pytest
from unittest.mock import patch, MagicMock
import openai
from ai_debug_assist import analyze_error_log, read_file

def test_read_file():
    with patch("os.path.exists", return_value=True):
        with patch("builtins.open", new_callable=MagicMock) as mock_open:
            mock_open.return_value.__enter__.return_value.read.return_value = "Sample error log content"
            content = read_file("dummy_path.log")
            assert content == "Sample error log content"

    with patch("os.path.exists", return_value=False):
        with pytest.raises(FileNotFoundError):
            read_file("non_existent_file.log")

@patch("openai.Completion.create")
def test_analyze_error_log(mock_openai):
    mock_openai.return_value.choices = [MagicMock(text="Debugging suggestion 1\nDebugging suggestion 2")]

    api_key = "dummy_api_key"
    error_log = "Sample error log"
    code_path = "./src"

    suggestions = analyze_error_log(api_key, error_log, code_path)
    assert "Debugging suggestion 1" in suggestions
    assert "Debugging suggestion 2" in suggestions

    mock_openai.side_effect = openai.error.OpenAIError("API error")
    suggestions = analyze_error_log(api_key, error_log, code_path)
    assert "Error communicating with OpenAI API" in suggestions