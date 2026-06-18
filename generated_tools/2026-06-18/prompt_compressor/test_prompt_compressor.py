import pytest
from unittest.mock import patch
from prompt_compressor import compress_prompt

def test_compress_prompt_empty_input():
    assert compress_prompt("") == ""

@patch("prompt_compressor.pipeline")
def test_compress_prompt_basic(mock_pipeline):
    mock_pipeline.return_value = lambda text, max_length, min_length, do_sample: [{"summary_text": "compressed text"}]
    result = compress_prompt("This is a long prompt that needs to be compressed.")
    assert result == "compressed text"

@patch("prompt_compressor.pipeline")
def test_compress_prompt_with_redundancy(mock_pipeline):
    mock_pipeline.return_value = lambda text, max_length, min_length, do_sample: [{"summary_text": text}]
    result = compress_prompt("This is a test. This is a test.")
    assert result == "This is a test."

@patch("prompt_compressor.pipeline")
def test_compress_prompt_with_verbosity(mock_pipeline):
    mock_pipeline.return_value = lambda text, max_length, min_length, do_sample: [{"summary_text": "short text" if max_length == 15 else "longer text"}]
    result = compress_prompt("This is a test.", verbosity=1)
    assert result == "short text"
    result = compress_prompt("This is a test.", verbosity=3)
    assert result == "longer text"