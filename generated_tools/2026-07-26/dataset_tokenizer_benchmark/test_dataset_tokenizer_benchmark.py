import pytest
from unittest.mock import patch, MagicMock
from dataset_tokenizer_benchmark import benchmark_tokenizer

def mock_open(*args, **kwargs):
    return MagicMock(readlines=lambda: ["This is a test.", "Another test line."])

@patch("builtins.open", new=mock_open)
@patch("psutil.Process")
@patch("transformers.AutoTokenizer.from_pretrained")
def test_benchmark_hf_tokenizer(mock_auto_tokenizer, mock_psutil):
    mock_tokenizer = MagicMock()
    mock_tokenizer.tokenize.side_effect = lambda x: x.split()
    mock_auto_tokenizer.return_value = mock_tokenizer
    mock_psutil.return_value.memory_info.return_value.rss = 1000000

    results = benchmark_tokenizer("mock_dataset.txt", ["hf_test-tokenizer"], batch_size=1)

    assert len(results) == 1
    assert results[0]["tokenizer"] == "hf_test-tokenizer"
    assert results[0]["time_taken"] > 0
    assert results[0]["memory_used"] >= 0

@patch("builtins.open", new=mock_open)
@patch("psutil.Process")
@patch("sentencepiece.SentencePieceProcessor")
def test_benchmark_sentencepiece(mock_sentencepiece, mock_psutil):
    mock_tokenizer = MagicMock()
    mock_tokenizer.EncodeAsPieces.side_effect = lambda x: x.split()
    mock_sentencepiece.return_value = mock_tokenizer
    mock_psutil.return_value.memory_info.return_value.rss = 1000000

    results = benchmark_tokenizer("mock_dataset.txt", ["sentencepiece"], batch_size=1)

    assert len(results) == 1
    assert results[0]["tokenizer"] == "sentencepiece"
    assert results[0]["time_taken"] > 0
    assert results[0]["memory_used"] >= 0

@patch("builtins.open", new=mock_open)
def test_benchmark_invalid_tokenizer():
    results = benchmark_tokenizer("mock_dataset.txt", ["invalid_tokenizer"], batch_size=1)

    assert len(results) == 0
