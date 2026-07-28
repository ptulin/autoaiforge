import pytest
from unittest.mock import patch, MagicMock
import torch
from llm_batch_tester import load_model, benchmark_model, run_benchmark

def test_load_model():
    with patch('torch.load', return_value=MagicMock()) as mock_load:
        model = load_model('fake_model_path')
        mock_load.assert_called_once_with('fake_model_path')
        assert model.eval.called

def test_benchmark_model():
    model = MagicMock()
    model.return_value = None
    latency, throughput = benchmark_model(model, batch_size=4, input_shape=(3, 224, 224), device='cpu')
    assert latency > 0
    assert throughput > 0

def test_run_benchmark():
    with patch('llm_batch_tester.load_model', return_value=MagicMock()) as mock_load_model:
        with patch('llm_batch_tester.benchmark_model', return_value=(0.1, 40.0)) as mock_benchmark:
            results = run_benchmark('fake_model_path', 1, 3, (3, 224, 224), 'cpu')
            assert len(results) == 3
            assert results[0] == (1, 0.1, 40.0)
            mock_load_model.assert_called_once()
            mock_benchmark.assert_called()
