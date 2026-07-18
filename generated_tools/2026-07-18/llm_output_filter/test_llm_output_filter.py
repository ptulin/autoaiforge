import pytest
from unittest.mock import patch, mock_open
import json
from llm_output_filter import filter_output

def test_filter_output_with_direct_rules():
    text = "My credit card number is 1234-5678-9012-3456."
    rules = {r"\b\d{4}-\d{4}-\d{4}-\d{4}\b": "[REDACTED]"}
    expected = "My credit card number is [REDACTED]."
    assert filter_output(text, rules=rules) == expected

def test_filter_output_with_rules_file():
    text = "My email is user@example.com."
    rules = {r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b": "[REDACTED]"}
    rules_json = json.dumps(rules)

    with patch("builtins.open", mock_open(read_data=rules_json)):
        expected = "My email is [REDACTED]."
        assert filter_output(text, rules_file="rules.json") == expected

def test_filter_output_with_invalid_regex():
    text = "Sensitive data here."
    rules = {r"[": "[REDACTED]"}  # Invalid regex
    with pytest.raises(ValueError, match="Invalid regex pattern"):
        filter_output(text, rules=rules)

def test_filter_output_with_empty_text():
    with pytest.raises(ValueError, match="Input text must be a non-empty string."):
        filter_output("", rules={})

def test_filter_output_with_invalid_rules_file():
    with patch("builtins.open", side_effect=FileNotFoundError):
        with pytest.raises(ValueError, match="Invalid rules file."):
            filter_output("Some text", rules_file="nonexistent.json")