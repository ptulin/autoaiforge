import pytest
import torch
from unittest.mock import patch, MagicMock
from model_pruning_analyzer import analyze_pruning, load_model, prune_model

@pytest.fixture
def mock_model():
    class MockModel(torch.nn.Module):
        def __init__(self):
            super().__init__()
            self.fc = torch.nn.Linear(10, 5)
            self.input_shape = (10,)

        def forward(self, x):
            return self.fc(x)

    return MockModel()

@patch("model_pruning_analyzer.load_model")
@patch("model_pruning_analyzer.calculate_model_size")
@patch("model_pruning_analyzer.measure_inference_speed")
def test_analyze_pruning(mock_measure_inference_speed, mock_calculate_model_size, mock_load_model, mock_model):
    mock_load_model.return_value = mock_model
    mock_calculate_model_size.side_effect = [1000, 800]  # Mock original and pruned sizes
    mock_measure_inference_speed.side_effect = [0.1, 0.08]  # Mock original and pruned speeds

    metrics = analyze_pruning("dummy_path", "structured", 0.5)

    assert metrics["original_size"] == 1000
    assert metrics["pruned_size"] == 800
    assert metrics["size_reduction_percent"] == 20.0
    assert metrics["original_inference_speed"] == 0.1
    assert metrics["pruned_inference_speed"] == 0.08
    assert metrics["speed_change_percent"] == -20.0

@patch("model_pruning_analyzer.prune.ln_structured")
def test_prune_model_structured(mock_ln_structured, mock_model):
    pruned_model = prune_model(mock_model, "structured", 0.5)
    assert isinstance(pruned_model, torch.nn.Module)
    mock_ln_structured.assert_called()

@patch("model_pruning_analyzer.prune.random_unstructured")
def test_prune_model_unstructured(mock_random_unstructured, mock_model):
    pruned_model = prune_model(mock_model, "unstructured", 0.5)
    assert isinstance(pruned_model, torch.nn.Module)
    mock_random_unstructured.assert_called()