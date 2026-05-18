import pytest
from unittest.mock import patch
import openai
from ai_snippet_suggester import generate_snippet

def test_generate_snippet_success():
    with patch("openai.Completion.create") as mock_create:
        mock_response = type("Response", (object,), {"choices": [type("Choice", (object,), {"text": "def example():\n    pass"})()]})
        mock_create.return_value = mock_response
        result = generate_snippet("Sort a list of integers", "python")
        assert result == "def example():\n    pass"

def test_generate_snippet_openai_error():
    with patch("openai.Completion.create", side_effect=openai.error.OpenAIError("API Error")):
        result = generate_snippet("Sort a list of integers", "python")
        assert result == "Error generating snippet: API Error"

def test_generate_snippet_generic_error():
    with patch("openai.Completion.create", side_effect=Exception("Generic Error")):
        result = generate_snippet("Sort a list of integers", "python")
        assert result == "Error generating snippet: Generic Error"

def test_generate_snippet_empty_description():
    with patch("openai.Completion.create") as mock_create:
        mock_response = type("Response", (object,), {"choices": [type("Choice", (object,), {"text": ""})()]})
        mock_create.return_value = mock_response
        result = generate_snippet("", "python")
        assert result == ""