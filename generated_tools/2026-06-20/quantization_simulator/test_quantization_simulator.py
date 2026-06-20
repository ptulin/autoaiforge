import pytest
import torch
from unittest.mock import patch, MagicMock
from quantization_simulator import simulate_quantization

def test_simulate_quantization_no_eval_data():
    model = torch.nn.Linear(10, 2)

    # Mock torch.cuda.is_available to simulate no CUDA environment
    with patch("torch.cuda.is_available", return_value=False):
        results = simulate_quantization(model, quantization_levels=[16, 8])

    assert 16 in results
    assert 8 in results
    assert results[16]["memory_usage_mb"] > 0
    assert results[8]["memory_usage_mb"] > 0
    assert results[16]["inference_time_ms"] is None
    assert results[8]["inference_time_ms"] is None

def test_simulate_quantization_with_eval_data():
    model = torch.nn.Linear(10, 2)
    eval_data = [(torch.randn(1, 10), torch.tensor([1]))]

    # Mock the forward method of the model
    with patch.object(torch.nn.Linear, "forward", return_value=torch.tensor([[0.1, 0.9]])):
        results = simulate_quantization(model, eval_data, quantization_levels=[8])

    assert 8 in results
    assert results[8]["accuracy"] == 1.0

def test_invalid_quantization_level():
    model = torch.nn.Linear(10, 2)
    with pytest.raises(ValueError):
        simulate_quantization(model, quantization_levels=[32])