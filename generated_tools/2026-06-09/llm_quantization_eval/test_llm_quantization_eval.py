import pytest
from unittest.mock import patch, MagicMock
import torch
from llm_quantization_eval import quantize_model, evaluate_model, benchmark_model

def test_quantize_model():
    model = MagicMock()
    quantized_model = quantize_model(model, "INT8")
    assert quantized_model is not None

    model = MagicMock()
    quantized_model = quantize_model(model, "FP16")
    assert quantized_model is not None

    with pytest.raises(ValueError):
        quantize_model(model, "INVALID")

@patch("llm_quantization_eval.AutoTokenizer.from_pretrained")
@patch("llm_quantization_eval.AutoModelForCausalLM.from_pretrained")
@patch("llm_quantization_eval.Dataset.from_dict")
def test_evaluate_model(mock_dataset, mock_model, mock_tokenizer):
    mock_model.return_value.generate.return_value = torch.tensor([[0]])
    mock_tokenizer.return_value.decode.return_value = "Artificial Intelligence"
    mock_dataset.return_value = [{"question": "What is AI?", "answers": {"text": ["Artificial Intelligence"]}}]

    model = mock_model.return_value
    tokenizer = mock_tokenizer.return_value
    dataset = mock_dataset.return_value

    accuracy = evaluate_model(model, tokenizer, dataset, "cpu")
    assert accuracy == 1.0

@patch("llm_quantization_eval.AutoTokenizer.from_pretrained")
@patch("llm_quantization_eval.AutoModelForCausalLM.from_pretrained")
@patch("llm_quantization_eval.Dataset.from_dict")
def test_benchmark_model(mock_dataset, mock_model, mock_tokenizer):
    mock_model.return_value.generate.return_value = torch.tensor([[0]])
    mock_dataset.return_value = [{"question": "What is AI?"}]

    model = mock_model.return_value
    tokenizer = mock_tokenizer.return_value
    dataset = mock_dataset.return_value

    elapsed_time, peak_memory = benchmark_model(model, tokenizer, dataset, "cpu")
    assert elapsed_time >= 0
    assert peak_memory == 0  # Since we're mocking and not using CUDA
