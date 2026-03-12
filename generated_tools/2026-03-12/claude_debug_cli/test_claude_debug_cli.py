import pytest
from unittest.mock import patch, mock_open
from claude_debug_cli import analyze_code
import openai

def test_analyze_code_file_not_found():
    with pytest.raises(FileNotFoundError):
        analyze_code("non_existent_file.py", "fake_api_key")

def test_analyze_code_empty_file():
    with patch("os.path.exists", return_value=True):  # Mock file existence
        with patch("builtins.open", mock_open(read_data="")):
            with pytest.raises(ValueError):
                analyze_code("empty_file.py", "fake_api_key")

def test_analyze_code_openai_error():
    with patch("os.path.exists", return_value=True):  # Mock file existence
        with patch("builtins.open", mock_open(read_data="print('Hello, World!')")):
            with patch("openai.ChatCompletion.create", side_effect=openai.error.OpenAIError("API error")):
                with pytest.raises(RuntimeError) as excinfo:
                    analyze_code("script.py", "fake_api_key")
                assert "OpenAI API error" in str(excinfo.value)
