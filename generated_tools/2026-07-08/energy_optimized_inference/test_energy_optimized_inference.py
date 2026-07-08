import pytest
import numpy as np
import torch
from unittest.mock import patch
from energy_optimized_inference import optimize_batch_size, monitor_energy_usage

def test_monitor_energy_usage():
    with patch("psutil.cpu_percent", return_value=50.0):
        energy_usage = monitor_energy_usage()
        assert energy_usage == 50.0

def test_optimize_batch_size():
    model = torch.nn.Linear(10, 1)
    data = np.random.rand(100, 10)

    with patch("energy_optimized_inference.monitor_energy_usage", return_value=10.0):
        batch_size, results = optimize_batch_size(model, data, min_batch=16, max_batch=32)
        assert batch_size >= 16
        assert batch_size <= 32
        assert results is not None

def test_optimize_batch_size_empty_data():
    model = torch.nn.Linear(10, 1)
    data = np.array([])

    with patch("energy_optimized_inference.monitor_energy_usage", return_value=10.0):
        batch_size, results = optimize_batch_size(model, data, min_batch=16, max_batch=32)
        assert batch_size == 16
        assert results is None