import pytest
from unittest.mock import patch, MagicMock
import torch
from llm_lazy_loader import LazyLoader

def test_lazy_loader_initialization():
    loader = LazyLoader("gpt2", memory_limit=2000)
    assert loader.model_name == "gpt2"
    assert loader.memory_limit == 2000
    assert loader.model is None
    assert loader.tokenizer is None

@patch("llm_lazy_loader.psutil.virtual_memory")
def test_memory_check_within_limit(mock_virtual_memory):
    mock_virtual_memory.return_value = MagicMock(available=3 * 1024 * 1024 * 1024)  # 3 GB available
    loader = LazyLoader("gpt2", memory_limit=2000)
    assert loader._check_memory() is True

@patch("llm_lazy_loader.psutil.virtual_memory")
def test_memory_check_exceeds_limit(mock_virtual_memory):
    mock_virtual_memory.return_value = MagicMock(available=500 * 1024 * 1024)  # 500 MB available
    loader = LazyLoader("gpt2", memory_limit=2000)
    assert loader._check_memory() is False

@patch("llm_lazy_loader.AutoTokenizer.from_pretrained")
@patch("llm_lazy_loader.AutoModel.from_pretrained")
@patch("llm_lazy_loader.psutil.virtual_memory")
def test_model_loading(mock_virtual_memory, mock_auto_model, mock_auto_tokenizer):
    mock_virtual_memory.return_value = MagicMock(available=3 * 1024 * 1024 * 1024)  # 3 GB available
    mock_auto_model.return_value = MagicMock()
    mock_auto_tokenizer.return_value = MagicMock()

    loader = LazyLoader("gpt2", memory_limit=2000)
    loader.load()

    mock_auto_model.assert_called_once_with("gpt2")
    mock_auto_tokenizer.assert_called_once_with("gpt2")
    assert loader.model is not None
    assert loader.tokenizer is not None

@patch("llm_lazy_loader.AutoTokenizer.from_pretrained")
@patch("llm_lazy_loader.AutoModel.from_pretrained")
@patch("llm_lazy_loader.psutil.virtual_memory")
def test_model_inference(mock_virtual_memory, mock_auto_model, mock_auto_tokenizer):
    mock_virtual_memory.return_value = MagicMock(available=3 * 1024 * 1024 * 1024)  # 3 GB available
    mock_model = MagicMock()
    mock_tokenizer = MagicMock()
    mock_auto_model.return_value = mock_model
    mock_auto_tokenizer.return_value = mock_tokenizer

    mock_tokenizer.return_value = {"input_ids": torch.tensor([[1, 2, 3]])}
    mock_model.return_value = MagicMock()

    loader = LazyLoader("gpt2", memory_limit=2000)
    loader.load()
    result = loader.generate("Hello, world!")

    mock_tokenizer.assert_called_once_with("Hello, world!", return_tensors="pt")
    mock_model.assert_called_once_with(input_ids=mock_tokenizer.return_value["input_ids"])
    assert result == mock_model.return_value