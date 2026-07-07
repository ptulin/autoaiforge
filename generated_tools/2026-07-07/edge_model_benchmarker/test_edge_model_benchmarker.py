import pytest
import torch
import numpy as np
from unittest.mock import patch, MagicMock
from edge_model_benchmarker import benchmark_model

def test_benchmark_model_success():
    model_path = "test_model.pth"
    dataset_path = "test_dataset.csv"

    # Mock model and dataset
    torch.save(torch.nn.Linear(10, 1), model_path)
    np.savetxt(dataset_path, np.random.rand(100, 11), delimiter=',')

    results = benchmark_model(model_path, dataset_path, cpu_cores=2, simulate_latency=50)

    assert "average_latency" in results
    assert "average_throughput" in results
    assert len(results["results"]) > 0

def test_benchmark_model_invalid_model():
    model_path = "invalid_model.pth"
    dataset_path = "test_dataset.csv"

    np.savetxt(dataset_path, np.random.rand(100, 11), delimiter=',')

    results = benchmark_model(model_path, dataset_path)

    assert "error" in results
    assert "Failed to load model" in results["error"]

def test_benchmark_model_invalid_dataset():
    model_path = "test_model.pth"
    dataset_path = "invalid_dataset.csv"

    torch.save(torch.nn.Linear(10, 1), model_path)

    results = benchmark_model(model_path, dataset_path)

    assert "error" in results
    assert "Failed to load dataset" in results["error"]
