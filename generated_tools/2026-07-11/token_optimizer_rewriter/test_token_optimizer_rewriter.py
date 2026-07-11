import pytest
from unittest.mock import patch, mock_open, MagicMock
from token_optimizer_rewriter import count_tokens, optimize_text, process_input

def test_count_tokens():
    text = "This is a test sentence."
    assert count_tokens(text) > 0

@patch("openai.ChatCompletion.create")
def test_optimize_text(mock_create):
    mock_create.return_value = MagicMock(
        choices=[MagicMock(message=MagicMock(content="Optimized text."))]
    )
    api_key = "test_api_key"
    input_text = "This is a test sentence."
    optimized_text = optimize_text(api_key, input_text)
    assert optimized_text == "Optimized text."

@patch("builtins.open", new_callable=mock_open, read_data="This is a test file.")
def test_process_input(mock_open):
    input_path = "test.txt"
    text = process_input(input_path)
    assert text == "This is a test file."
    mock_open.assert_called_once_with(input_path, "r", encoding="utf-8")