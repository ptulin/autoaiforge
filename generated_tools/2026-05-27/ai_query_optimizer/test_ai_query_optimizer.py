import pytest
from unittest.mock import patch, MagicMock
from ai_query_optimizer import optimize_query, save_output
import json
import openai

def test_optimize_query_success():
    mock_response = MagicMock()
    mock_response.choices = [MagicMock(text="Optimized query example")]

    with patch("openai.Completion.create", return_value=mock_response):
        result = optimize_query("example query", "fake_api_key")
        assert result == "Optimized query example"

def test_optimize_query_empty():
    with pytest.raises(ValueError, match="Query cannot be empty."):
        optimize_query("", "fake_api_key")

def test_optimize_query_api_error():
    with patch("openai.Completion.create", side_effect=openai.error.OpenAIError("API error")):
        with pytest.raises(RuntimeError, match="Failed to optimize query: API error"):
            optimize_query("example query", "fake_api_key")

def test_save_output_json(tmp_path):
    output_path = tmp_path / "output.json"
    save_output("Optimized query", output_path, "json")
    with open(output_path, "r") as f:
        data = json.load(f)
        assert data == {"optimized_query": "Optimized query"}

def test_save_output_text(tmp_path):
    output_path = tmp_path / "output.txt"
    save_output("Optimized query", output_path, "text")
    with open(output_path, "r") as f:
        data = f.read()
        assert data == "Optimized query"