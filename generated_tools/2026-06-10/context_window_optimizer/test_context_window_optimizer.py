import pytest
from unittest.mock import patch, mock_open
from context_window_optimizer import estimate_token_count, summarize_text, process_input

def test_estimate_token_count():
    tokenizer_mock = patch("context_window_optimizer.GPT2Tokenizer.from_pretrained").start()
    tokenizer_mock.return_value.tokenize.return_value = ["token1", "token2", "token3"]

    text = "This is a test."
    count = estimate_token_count(text)
    assert count == 3

    tokenizer_mock.stop()

def test_summarize_text():
    tokenizer_mock = patch("context_window_optimizer.GPT2Tokenizer.from_pretrained").start()
    tokenizer_mock.return_value.tokenize.side_effect = lambda x: x.split()

    text = "This is a test. This is another sentence."
    result = summarize_text(text, max_tokens=5)
    assert result == "This is a test."

    result = summarize_text(text, max_tokens=10)
    assert result == "This is a test. This is another sentence."

    tokenizer_mock.stop()

def test_process_input_file():
    tokenizer_mock = patch("context_window_optimizer.GPT2Tokenizer.from_pretrained").start()
    tokenizer_mock.return_value.tokenize.side_effect = lambda x: x.split()

    mock_file_content = "This is a test. This is another sentence."
    with patch("builtins.open", mock_open(read_data=mock_file_content)):
        with patch("os.path.isfile", return_value=True):
            result = process_input("dummy_file.txt", max_tokens=5, model_name="gpt2")
            assert result == "This is a test."

    tokenizer_mock.stop()

def test_process_input_string():
    tokenizer_mock = patch("context_window_optimizer.GPT2Tokenizer.from_pretrained").start()
    tokenizer_mock.return_value.tokenize.side_effect = lambda x: x.split()

    text = "This is a test. This is another sentence."
    result = process_input(text, max_tokens=5, model_name="gpt2")
    assert result == "This is a test."

    tokenizer_mock.stop()

def test_empty_input():
    with pytest.raises(ValueError, match="Input text is empty."):
        process_input("", max_tokens=10, model_name="gpt2")
