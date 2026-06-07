import pytest
from unittest.mock import patch, MagicMock
from quantization_benchmark import load_model, apply_quantization, benchmark_model

def test_load_model():
    with patch("quantization_benchmark.AutoTokenizer.from_pretrained") as mock_tokenizer, \
         patch("quantization_benchmark.AutoModelForCausalLM.from_pretrained") as mock_model:
        mock_tokenizer.return_value = MagicMock()
        mock_model.return_value = MagicMock()

        model, tokenizer = load_model("dummy_model_path")

        mock_tokenizer.assert_called_once_with("dummy_model_path")
        mock_model.assert_called_once_with("dummy_model_path")
        assert model is not None
        assert tokenizer is not None

def test_apply_quantization():
    model = MagicMock()

    # Test GGUF
    quantized_model = apply_quantization(model, "GGUF")
    assert quantized_model is not None

    # Test unsupported method
    with pytest.raises(ValueError):
        apply_quantization(model, "INVALID")

def test_benchmark_model():
    model = MagicMock()
    tokenizer = MagicMock()
    tokenizer.return_value = {"input_ids": [1, 2, 3]}
    model.generate = MagicMock()

    dataset = ["Sample input"]
    metrics = benchmark_model(model, tokenizer, dataset)

    assert "memory_usage" in metrics
    assert "inference_time" in metrics
    assert "accuracy" in metrics
    assert metrics["accuracy"] >= 0.8
    assert metrics["accuracy"] <= 0.95