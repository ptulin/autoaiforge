import pytest
from unittest.mock import MagicMock
from token_efficiency_optimizer import optimize_tokens

def test_optimize_tokens_empty_input():
    tokenizer_mock = MagicMock()
    tokenizer_mock.return_value = {"input_ids": []}

    with pytest.raises(ValueError, match="Input text cannot be empty."):
        optimize_tokens("", tokenizer_mock)

def test_optimize_tokens_invalid_memory():
    tokenizer_mock = MagicMock()
    tokenizer_mock.return_value = {"input_ids": [1, 2, 3]}

    with pytest.raises(ValueError, match="Max memory must be greater than 0."):
        optimize_tokens("test", tokenizer_mock, max_memory=0)

def test_optimize_tokens_valid_input():
    tokenizer_mock = MagicMock()
    tokenizer_mock.return_value = {"input_ids": [[1, 2, 3, 4, 5, 6, 7, 8, 9, 10]]}

    result = optimize_tokens("test", tokenizer_mock, max_memory=1)

    # Assuming 100,000 tokens per GB, 1 GB allows 100,000 tokens
    # The input has only 10 tokens, so it should return a single batch
    assert result == [[1, 2, 3, 4, 5, 6, 7, 8, 9, 10]]

def test_optimize_tokens_multiple_batches():
    tokenizer_mock = MagicMock()
    tokenizer_mock.return_value = {"input_ids": [[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]]}

    result = optimize_tokens("test", tokenizer_mock, max_memory=1)

    # Assuming 100,000 tokens per GB, 1 GB allows 100,000 tokens
    # The input has 15 tokens, so it should return one batch (since max_tokens > len(input_ids))
    assert result == [[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]]