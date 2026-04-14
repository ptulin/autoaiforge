import pytest
from unittest.mock import patch
from ai_payload_sanitizer import sanitize

def test_sanitize_string():
    input_data = "DROP DATABASE"
    expected_output = "[REDACTED]"
    assert sanitize(input_data) == expected_output

def test_sanitize_json():
    input_data = {"query": "DROP DATABASE", "safe": "SELECT *"}
    expected_output = {"query": "[REDACTED]", "safe": "[REDACTED]"}
    assert sanitize(input_data) == expected_output

def test_sanitize_custom_rules():
    input_data = "DELETE FROM users"
    rules = {r"(?i)delete\s+from": "REMOVED"}
    expected_output = "REMOVED users"
    assert sanitize(input_data, rules) == expected_output

def test_sanitize_nested_json():
    input_data = {"query": {"subquery": "DROP DATABASE"}, "safe": "SELECT *"}
    expected_output = {"query": {"subquery": "[REDACTED]"}, "safe": "[REDACTED]"}
    assert sanitize(input_data) == expected_output

def test_sanitize_invalid_payload():
    with pytest.raises(ValueError):
        sanitize(12345)