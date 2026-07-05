import pytest
from unittest.mock import patch, MagicMock
from ai_code_snippet_optimizer import optimize_code
import openai

def test_optimize_code_success():
    mock_response = {
        'choices': [
            {
                'message': {
                    'content': "def optimized_function():\n    pass\n\nExplanation: Simplified the function for better readability."
                }
            }
        ]
    }

    with patch('openai.ChatCompletion.create', return_value=mock_response):
        with patch.dict('os.environ', {"OPENAI_API_KEY": "test_key"}):
            result = optimize_code("def example_function():\n    pass")
            assert result["optimized_code"] == "def optimized_function():\n    pass"
            assert result["explanation"] == "Simplified the function for better readability."

def test_optimize_code_empty_input():
    with pytest.raises(ValueError, match="The code snippet cannot be empty."):
        optimize_code("")

def test_optimize_code_missing_api_key():
    with patch.dict('os.environ', {}, clear=True):
        with pytest.raises(EnvironmentError, match="OPENAI_API_KEY environment variable is not set."):
            optimize_code("print('Hello, World!')")

def test_optimize_code_api_error():
    with patch('openai.ChatCompletion.create', side_effect=openai.error.OpenAIError("API error")):
        with patch.dict('os.environ', {"OPENAI_API_KEY": "test_key"}):
            with pytest.raises(RuntimeError, match="An error occurred while communicating with the OpenAI API: API error"):
                optimize_code("print('Hello, World!')")