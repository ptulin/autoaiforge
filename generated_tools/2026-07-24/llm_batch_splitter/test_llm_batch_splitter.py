import pytest
from unittest.mock import MagicMock, patch
from llm_batch_splitter import process_in_chunks

def test_process_in_chunks_empty_inputs():
    """Test with empty input list."""
    mock_model = MagicMock()
    mock_tokenizer = MagicMock()

    result = process_in_chunks(mock_model, mock_tokenizer, inputs=[])
    assert result == []

def test_process_in_chunks_single_chunk():
    """Test with inputs that fit in a single chunk."""
    mock_model = MagicMock()
    mock_tokenizer = MagicMock()

    mock_tokenizer.return_tensors = "pt"
    mock_tokenizer.batch_decode.return_value = ["output1", "output2"]

    mock_model.no_grad.return_value.__enter__.return_value = None
    mock_model.return_value.logits.argmax.return_value = [0, 1]

    inputs = ["input1", "input2"]
    result = process_in_chunks(mock_model, mock_tokenizer, inputs, max_chunk_size=5)
    assert result == ["output1", "output2"]

def test_process_in_chunks_multiple_chunks():
    """Test with inputs that require multiple chunks."""
    mock_model = MagicMock()
    mock_tokenizer = MagicMock()

    mock_tokenizer.return_tensors = "pt"
    mock_tokenizer.batch_decode.side_effect = [["output1", "output2"], ["output3"]]

    mock_model.no_grad.return_value.__enter__.return_value = None
    mock_model.return_value.logits.argmax.side_effect = [[0, 1], [2]]

    inputs = ["input1", "input2", "input3"]
    result = process_in_chunks(mock_model, mock_tokenizer, inputs, max_chunk_size=2)
    assert result == ["output1", "output2", "output3"]
