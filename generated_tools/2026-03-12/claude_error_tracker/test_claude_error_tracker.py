import pytest
from unittest.mock import patch, MagicMock
from claude_error_tracker import ClaudeTracker
import traceback

@patch("claude_error_tracker.ChatCompletion.create")
def test_analyze_error_with_claude(mock_create):
    mock_create.return_value = {
        'choices': [{'message': {'content': 'This is a suggestion from Claude.'}}]
    }

    tracker = ClaudeTracker(api_key="test_api_key")
    error_message = "Traceback (most recent call last):\n  File \"<stdin>\", line 1, in <module>\nValueError: test error"
    suggestions = tracker._analyze_error_with_claude(error_message)

    assert suggestions == "This is a suggestion from Claude."
    mock_create.assert_called_once()

@patch("claude_error_tracker.ChatCompletion.create")
def test_analyze_error_with_claude_api_error(mock_create):
    mock_create.side_effect = Exception("API error")

    tracker = ClaudeTracker(api_key="test_api_key")
    error_message = "Traceback (most recent call last):\n  File \"<stdin>\", line 1, in <module>\nValueError: test error"

    with pytest.raises(RuntimeError, match="Error communicating with Claude API: API error"):
        tracker._analyze_error_with_claude(error_message)

@patch("claude_error_tracker.ClaudeTracker._analyze_error_with_claude")
def test_handle_exception(mock_analyze):
    mock_analyze.return_value = "Mocked suggestion."

    tracker = ClaudeTracker(api_key="test_api_key")
    with patch("claude_error_tracker.logging.Logger.error") as mock_logger_error, \
         patch("claude_error_tracker.logging.Logger.info") as mock_logger_info:

        try:
            raise ValueError("Test exception")
        except ValueError as e:
            error_message = ''.join(traceback.format_exception(type(e), e, e.__traceback__))
            tracker._handle_exception(type(e), e, e.__traceback__)

            mock_logger_error.assert_called_with("Unhandled exception captured:\n%s", error_message)
            mock_logger_info.assert_called_with("Claude's suggestions:\n%s", "Mocked suggestion.")