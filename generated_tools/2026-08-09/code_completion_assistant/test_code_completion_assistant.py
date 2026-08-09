import pytest
from unittest.mock import patch, Mock
from code_completion_assistant import get_code_completions, LanguageTool

@pytest.fixture
def mock_language_tool():
    with patch('code_completion_assistant.LanguageTool') as mock_tool:
        yield mock_tool

def test_get_code_completions_empty_code_context(mock_language_tool):
    code_context = ''
    cursor_position = 0
    completions = get_code_completions(code_context, cursor_position)
    assert completions == []

def test_get_code_completions_valid_code_context(mock_language_tool):
    code_context = 'print("Hello World")'
    cursor_position = 10
    mock_suggestion = Mock(offset=0, length=10)
    mock_language_tool.return_value.check.return_value = [mock_suggestion]
    completions = get_code_completions(code_context, cursor_position)
    assert len(completions) == 1

def test_get_code_completions_invalid_cursor_position(mock_language_tool):
    code_context = 'print("Hello World")'
    cursor_position = -1
    completions = get_code_completions(code_context, cursor_position)
    assert completions == []