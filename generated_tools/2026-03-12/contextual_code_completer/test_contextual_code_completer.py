import pytest
from unittest.mock import patch, mock_open
from contextual_code_completer import analyze_codebase, generate_code

def test_analyze_codebase_empty_directory(tmp_path):
    """Test analyze_codebase with an empty directory."""
    result = analyze_codebase(tmp_path)
    assert result == ""

def test_analyze_codebase_with_files(tmp_path):
    """Test analyze_codebase with Python files in the directory."""
    file_path = tmp_path / "test_file.py"
    file_path.write_text("def test_function():\n    pass")
    result = analyze_codebase(tmp_path)
    assert "def test_function()" in result

@patch("openai.Completion.create")
def test_generate_code(mock_openai):
    """Test generate_code with a mocked OpenAI API response."""
    mock_openai.return_value = {
        "choices": [{"text": "def generated_function():\n    pass"}]
    }
    context = "def existing_function():\n    pass"
    query = "Generate a new function"
    result = generate_code(context, query)
    assert "def generated_function()" in result
    mock_openai.assert_called_once()

@patch("openai.Completion.create")
def test_generate_code_error_handling(mock_openai):
    """Test generate_code handles errors from OpenAI API."""
    mock_openai.side_effect = Exception("API error")
    context = "def existing_function():\n    pass"
    query = "Generate a new function"
    with pytest.raises(RuntimeError, match="Error generating code: API error"):
        generate_code(context, query)