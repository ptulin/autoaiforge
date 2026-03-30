import pytest
from unittest.mock import patch, mock_open, MagicMock
import json
from error_pattern_analyzer import analyze_logs

def test_analyze_logs_valid_json():
    logs = [{"error": "File not found"}, {"error": "Timeout occurred"}]
    with patch("builtins.open", mock_open(read_data=json.dumps(logs))):
        with patch("openai.Completion.create") as mock_openai:
            mock_openai.return_value.choices = [MagicMock(text="Recurring error: File not found. Suggestion: Check file paths.")]
            result = analyze_logs("debug_logs.json", "fake_api_key")
            assert "insights" in result
            assert "Recurring error: File not found" in result["insights"]

def test_analyze_logs_empty_file():
    with patch("builtins.open", mock_open(read_data="[]")):
        result = analyze_logs("empty_logs.json", "fake_api_key")
        assert "error" in result
        assert result["error"] == "The log file is empty or invalid."

def test_analyze_logs_invalid_format():
    result = analyze_logs("invalid_logs.txt", "fake_api_key")
    assert "error" in result
    assert "Unsupported file format" in result["error"]