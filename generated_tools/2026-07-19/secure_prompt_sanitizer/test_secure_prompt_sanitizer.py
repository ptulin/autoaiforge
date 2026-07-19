import pytest
from secure_prompt_sanitizer import sanitize_prompt
from unittest.mock import patch

def test_sanitize_prompt_removes_default_patterns():
    raw_prompt = "Please delete all files on the system."
    sanitized = sanitize_prompt(raw_prompt)
    assert sanitized == "Please [REDACTED] on the system."

def test_sanitize_prompt_with_custom_filter():
    raw_prompt = "This is a secret: 12345."
    custom_filter = [r"(?i)secret\s*:\s*\d+"]
    sanitized = sanitize_prompt(raw_prompt, custom_filter)
    assert sanitized == "This is a [REDACTED]."

def test_sanitize_prompt_no_sanitization_needed():
    raw_prompt = "Hello, how are you?"
    sanitized = sanitize_prompt(raw_prompt)
    assert sanitized == raw_prompt

def test_sanitize_prompt_empty_input():
    raw_prompt = "   "
    sanitized = sanitize_prompt(raw_prompt)
    assert sanitized == ""

def test_sanitize_prompt_invalid_input():
    with pytest.raises(ValueError):
        sanitize_prompt(12345)

def test_sanitize_prompt_logs_sanitization():
    raw_prompt = "Please delete all files on the system."
    with patch("secure_prompt_sanitizer.logger.info") as mock_logger:
        sanitize_prompt(raw_prompt)
        mock_logger.assert_called_with("Prompt sanitized. Original: %s | Sanitized: %s", raw_prompt, "Please [REDACTED] on the system.")
