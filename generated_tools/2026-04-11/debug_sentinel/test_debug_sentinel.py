import pytest
import json
from unittest.mock import patch
from debug_sentinel import DebugSentinel

@pytest.fixture
def mock_openai_response():
    return {
        "choices": [
            {
                "message": {
                    "content": "This error occurs because you are trying to access a key that does not exist in the dictionary. Consider using the .get() method or checking if the key exists before accessing it."
                }
            }
        ]
    }

def test_suggest_fix_text_format(mock_openai_response):
    with patch("openai.ChatCompletion.create", return_value=mock_openai_response):
        sentinel = DebugSentinel(api_key="fake_api_key")
        stack_trace = "KeyError: 'nonexistent_key'"
        result = sentinel.suggest_fix(stack_trace, output_format="text")
        assert "This error occurs because" in result

def test_suggest_fix_json_format(mock_openai_response):
    with patch("openai.ChatCompletion.create", return_value=mock_openai_response):
        sentinel = DebugSentinel(api_key="fake_api_key")
        stack_trace = "KeyError: 'nonexistent_key'"
        result = sentinel.suggest_fix(stack_trace, output_format="json")
        parsed_result = json.loads(result)
        assert "suggestions" in parsed_result
        assert "This error occurs because" in parsed_result["suggestions"]

def test_suggest_fix_empty_stack_trace():
    sentinel = DebugSentinel(api_key="fake_api_key")
    with pytest.raises(ValueError, match="Stack trace cannot be empty."):
        sentinel.suggest_fix("", output_format="text")