import pytest
import torch
from unittest.mock import patch, MagicMock
from edge_inference_profiler import profile_model

def test_profile_model_valid():
    model = torch.nn.Linear(10, 1)
    torch.save(model, "test_model.pth")

    with patch("torch.load", return_value=model), \
         patch("torch.cuda.is_available", return_value=False):
        results = profile_model("test_model.pth", (1, 10), "test_graph.png")
        assert "latency_ms" in results
        assert "memory_mb" in results
        assert results["latency_ms"] > 0
        assert results["memory_mb"] == 0  # No CUDA, so memory usage should be 0

def test_profile_model_invalid_model():
    with pytest.raises(ValueError, match="Failed to load model"):
        profile_model("invalid_model.pth", (1, 10), "test_graph.png")

def test_profile_model_invalid_input_shape():
    model = torch.nn.Linear(10, 1)
    torch.save(model, "test_model.pth")

    with patch("torch.load", return_value=model):
        with pytest.raises(ValueError, match="Invalid input shape"):
            profile_model("test_model.pth", "invalid_shape", "test_graph.png")
