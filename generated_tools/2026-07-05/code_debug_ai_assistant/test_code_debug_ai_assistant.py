import pytest
from unittest.mock import patch, MagicMock
from code_debug_ai_assistant import get_debugging_suggestions

# Mock OpenAI API response
@pytest.fixture
def mock_openai_response():
    return {
        'choices': [
            {
                'message': {
                    'content': "Here are some debugging suggestions."
                }
            }
        ]
    }

@patch('code_debug_ai_assistant.openai.ChatCompletion.create')
def test_get_debugging_suggestions_success(mock_create, mock_openai_response):
    # Arrange
    mock_create.return_value = mock_openai_response
    input_text = "Traceback (most recent call last):\n  File \"<stdin>\", line 1, in <module>\nZeroDivisionError: division by zero"

    # Act
    result = get_debugging_suggestions(input_text)

    # Assert
    assert "suggestions" in result
    assert result["suggestions"] == "Here are some debugging suggestions."

@patch('code_debug_ai_assistant.openai.ChatCompletion.create')
def test_get_debugging_suggestions_api_error(mock_create):
    # Arrange
    mock_create.side_effect = Exception("API error")
    input_text = "print(1/0)"

    # Act
    result = get_debugging_suggestions(input_text)

    # Assert
    assert "error" in result
    assert result["error"] == "API error"

@patch('code_debug_ai_assistant.openai.ChatCompletion.create')
def test_get_debugging_suggestions_empty_input(mock_create):
    # Arrange
    mock_create.return_value = {
        'choices': [
            {
                'message': {
                    'content': "No input provided."
                }
            }
        ]
    }
    input_text = ""

    # Act
    result = get_debugging_suggestions(input_text)

    # Assert
    assert "suggestions" in result
    assert result["suggestions"] == "No input provided."
