import pytest
from unittest.mock import patch, MagicMock
import ide_ai_debug_helper
import sys

@pytest.fixture
def mock_openai():
    with patch("ide_ai_debug_helper.ChatCompletion.create") as mock:
        mock.return_value = {
            'choices': [
                {'message': {'content': 'This is a mock response from Claude AI.'}}
            ]
        }
        yield mock

def test_analyze_exception(mock_openai):
    helper = ide_ai_debug_helper.IDEAIDebugHelper(api_key="test_key")

    exc_type = ValueError
    exc_value = ValueError("Test error")
    exc_traceback = None

    with patch("builtins.print") as mock_print:
        helper.analyze_exception(exc_type, exc_value, exc_traceback)

        assert mock_openai.called
        mock_print.assert_any_call("Analyzing exception with Claude AI...\n")
        mock_print.assert_any_call("Claude AI Suggestions:\n")

def test_query_claude_ai(mock_openai):
    helper = ide_ai_debug_helper.IDEAIDebugHelper(api_key="test_key")
    response = helper._query_claude_ai("Sample traceback")

    assert response == "This is a mock response from Claude AI."
    mock_openai.assert_called_once()

def test_start():
    with patch("sys.excepthook", new_callable=MagicMock) as mock_excepthook:
        ide_ai_debug_helper.start(api_key="test_key")

        assert sys.excepthook == ide_ai_debug_helper._debug_helper_instance.analyze_exception
