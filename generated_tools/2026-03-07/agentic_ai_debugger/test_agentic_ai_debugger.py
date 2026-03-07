import pytest
from unittest.mock import patch, mock_open
from agentic_ai_debugger import AgenticAIDebugger

def test_analyze_code():
    debugger = AgenticAIDebugger(api_key="fake-api-key")
    with patch("openai.Completion.create") as mock_openai:
        mock_openai.return_value = {"choices": [{"text": "Suggested fix"}]}
        result = debugger.analyze_code("print(1/0)", "ZeroDivisionError")
        assert result == "Suggested fix"

def test_process_file():
    debugger = AgenticAIDebugger(api_key="fake-api-key", auto_apply=False)
    mock_code = "print(1/0)"
    with patch("builtins.open", mock_open(read_data=mock_code)) as mock_file:
        with patch("agentic_ai_debugger.AgenticAIDebugger.analyze_code", return_value="Suggested fix") as mock_analyze:
            with patch("os.path.isfile", return_value=True):
                debugger.process_file("test.py", "ZeroDivisionError")
                mock_file.assert_called_with("test.py", "r")
                mock_analyze.assert_called_once_with(mock_code, "ZeroDivisionError")

def test_apply_fix():
    debugger = AgenticAIDebugger(api_key="fake-api-key", auto_apply=True)
    mock_code = "print(1/0)"
    with patch("builtins.open", mock_open(read_data=mock_code)) as mock_file:
        debugger.apply_fix("test.py", "# This is a fix")
        mock_file().write.assert_called_with(mock_code + "\n\n# Suggested Fix:\n# This is a fix")
