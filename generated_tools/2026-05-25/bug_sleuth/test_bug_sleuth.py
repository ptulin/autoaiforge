import pytest
from unittest.mock import patch, MagicMock
from bug_sleuth import analyze_code
import openai

def test_analyze_code_with_valid_file(tmp_path):
    # Create a temporary Python file
    code = """def add(a, b):\n    return a + b\n"""
    file_path = tmp_path / "test_script.py"
    file_path.write_text(code)

    # Mock OpenAI API response
    with patch("openai.ChatCompletion.create") as mock_openai:
        mock_openai.return_value = {
            'choices': [{
                'message': {
                    'content': "No issues detected."
                }
            }]
        }

        result = analyze_code(str(file_path))
        assert "analysis" in result
        assert result["analysis"] == "No issues detected."

def test_analyze_code_with_invalid_code():
    code = "def add(a, b):\nreturn a + b"  # Invalid indentation

    result = analyze_code(code)
    assert "error" in result
    assert result["error"] == "Invalid Python code."

def test_analyze_code_with_openai_error():
    code = "def add(a, b):\n    return a + b"

    # Mock OpenAI API to raise an OpenAIError
    with patch("openai.ChatCompletion.create", side_effect=openai.error.OpenAIError("API error")) as mock_openai:
        result = analyze_code(code)
        assert "error" in result
        assert result["error"] == "OpenAI API error."
        assert "API error" in result["details"]