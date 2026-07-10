import pytest
from unittest.mock import patch, MagicMock
import torch
import numpy as np
from llm_perf_benchmark import benchmark_model, plot_metrics

def test_benchmark_model():
    mock_model = MagicMock()
    mock_model.eval = MagicMock()
    mock_model.return_value = None

    with patch('torch.jit.load', return_value=mock_model):
        metrics = benchmark_model("dummy_model.pt", "cpu", 16, 128)
        assert "average_latency" in metrics
        assert "throughput" in metrics
        assert len(metrics["latencies"]) == 10

def test_plot_metrics(tmp_path):
    latencies = [0.1, 0.2, 0.15, 0.12]
    output_file = tmp_path / "latency_plot.png"
    plot_metrics(latencies, output_file)
    assert output_file.exists()

def test_benchmark_model_invalid_model():
    with patch('torch.jit.load', side_effect=RuntimeError("Invalid model")):
        with pytest.raises(RuntimeError, match="Error during benchmarking: Invalid model"):
            benchmark_model("invalid_model.pt", "cpu", 16, 128)
