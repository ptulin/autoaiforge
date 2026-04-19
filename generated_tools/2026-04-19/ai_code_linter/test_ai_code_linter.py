import pytest
from unittest.mock import patch, mock_open
from ai_code_linter import AICodeLinter

def test_lint_code_file_not_found():
    linter = AICodeLinter(api_key="test_key")
    with pytest.raises(FileNotFoundError):
        linter.lint_code("non_existent_file.py")

@patch("os.path.exists", return_value=True)
@patch("pylint.lint.Run")
def test_lint_code(mock_pylint_run, mock_exists):
    mock_pylint_run.return_value.linter.reporter.messages = [
        type("Message", (object,), {"category": "convention", "module": "test_module", "line": 1, "msg": "Sample pylint issue"})()
    ]
    linter = AICodeLinter(api_key="test_key")
    result = linter.lint_code("test_file.py")
    assert result == [
        {
            "type": "convention",
            "module": "test_module",
            "line": 1,
            "message": "Sample pylint issue"
        }
    ]

@patch("openai.Completion.create")
def test_analyze_with_ai(mock_openai_create):
    mock_openai_create.return_value = {
        "choices": [{"text": "AI analysis result"}]
    }
    linter = AICodeLinter(api_key="test_key")
    result = linter.analyze_with_ai("print('Hello, world!')")
    assert result == "AI analysis result"
