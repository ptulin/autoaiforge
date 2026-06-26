import pytest
from unittest.mock import patch, mock_open
from content_guardrail_builder import ContentGuardrailBuilder

def mock_config():
    return {
        "keywords": ["badword"],
        "regex_patterns": ["\\bbad\\b"]
    }

@patch("builtins.open", new_callable=mock_open, read_data="keywords:\n  - badword\nregex_patterns:\n  - \\\\bbad\\\\b\n")
@patch("yaml.safe_load", return_value=mock_config())
def test_load_config(mock_yaml, mock_file):
    builder = ContentGuardrailBuilder("test_config.yaml")
    assert builder.config == {"keywords": ["badword"], "regex_patterns": ["\\bbad\\b"]}

@patch("builtins.open", new_callable=mock_open, read_data="keywords:\n  - badword\nregex_patterns:\n  - \\\\bbad\\\\b\n")
@patch("yaml.safe_load", return_value=mock_config())
def test_filter_content_keywords(mock_yaml, mock_file):
    builder = ContentGuardrailBuilder("test_config.yaml")
    content = "badword"
    sanitized, diagnostics = builder.filter_content(content)
    assert sanitized == "[REDACTED]"
    assert "Keyword match: badword" in diagnostics

@patch("builtins.open", new_callable=mock_open, read_data="keywords:\n  - badword\nregex_patterns:\n  - \\\\bbad\\\\b\n")
@patch("yaml.safe_load", return_value=mock_config())
def test_filter_content_regex(mock_yaml, mock_file):
    builder = ContentGuardrailBuilder("test_config.yaml")
    content = "bad"
    sanitized, diagnostics = builder.filter_content(content)
    assert sanitized == "[REDACTED]"
    assert "Regex match: \\bbad\\b" in diagnostics

@patch("content_guardrail_builder.ContentGuardrailBuilder._load_ml_model", return_value=None)
@patch("builtins.open", new_callable=mock_open, read_data="keywords:\n  - badword\nregex_patterns:\n  - \\\\bbad\\\\b\n")
@patch("yaml.safe_load", return_value=mock_config())
def test_no_ml_model(mock_yaml, mock_file, mock_ml_model):
    builder = ContentGuardrailBuilder("test_config.yaml")
    content = "This is a test with badword and bad."
    sanitized, diagnostics = builder.filter_content(content)
    assert sanitized == "This is a test with [REDACTED] and [REDACTED]."
    assert len(diagnostics) == 2
    assert "Keyword match: badword" in diagnostics
    assert "Regex match: \\bbad\\b" in diagnostics