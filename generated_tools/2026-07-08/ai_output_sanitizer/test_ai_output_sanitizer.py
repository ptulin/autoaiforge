import pytest
from unittest.mock import mock_open, patch
from ai_output_sanitizer import sanitize_text, load_rules

def test_sanitize_text_mask():
    text = "This is a secret API key: 12345-ABCDE"
    rules = [{"pattern": "\\d{5}-[A-Z]{5}", "description": "API Key"}]
    sanitized_text, flagged_items = sanitize_text(text, rules, mask=True)

    assert sanitized_text == "This is a secret API key: [REDACTED]"
    assert flagged_items == [("12345-ABCDE", "API Key")]

def test_sanitize_text_flag():
    text = "Visit http://private-url.com for details."
    rules = [{"pattern": "http://[a-zA-Z0-9.-]+", "description": "Private URL"}]
    sanitized_text, flagged_items = sanitize_text(text, rules, mask=False)

    assert sanitized_text == text
    assert flagged_items == [("http://private-url.com", "Private URL")]

def test_load_rules():
    mock_rules = '[{"pattern": "\\\\d{5}-[A-Z]{5}", "description": "API Key"}]'

    with patch("builtins.open", mock_open(read_data=mock_rules)):
        rules = load_rules("rules.json")

    assert rules == [{"pattern": "\\d{5}-[A-Z]{5}", "description": "API Key"}]
