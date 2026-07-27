import pytest
import torch
from unittest.mock import patch, MagicMock
from distilled_model_evaluator import load_model, evaluate_model, memory_usage


def test_load_model():
    with patch("torch.load") as mock_torch_load:
        mock_model = MagicMock()
        mock_torch_load.return_value = mock_model

        model = load_model("dummy_path.pth")
        assert model == mock_model
        mock_torch_load.assert_called_once_with("dummy_path.pth")


def test_evaluate_model():
    mock_model = MagicMock()
    mock_model.return_value = torch.tensor([[0.1, 0.9], [0.8, 0.2]])

    data_loader = [
        (torch.tensor([[1.0, 2.0], [3.0, 4.0]]), torch.tensor([1, 0]))
    ]

    metrics = evaluate_model(mock_model, data_loader)
    assert "accuracy" in metrics
    assert "avg_latency" in metrics
    assert metrics["accuracy"] == 1.0


def test_memory_usage():
    mock_model = MagicMock()
    mock_model.parameters.return_value = [
        torch.tensor([1.0, 2.0, 3.0]),
        torch.tensor([4.0, 5.0])
    ]

    memory = memory_usage(mock_model)
    assert memory > 0
    assert isinstance(memory, float)