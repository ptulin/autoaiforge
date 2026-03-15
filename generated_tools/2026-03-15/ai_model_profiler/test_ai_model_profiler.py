import pytest
from unittest.mock import patch, MagicMock
from ai_model_profiler import analyze_pytorch_model, analyze_tensorflow_model, generate_visualization
import os

def test_analyze_pytorch_model():
    with patch("torch.load") as mock_torch_load:
        mock_model = MagicMock()
        mock_model.named_modules.return_value = [
            ("layer1", MagicMock(parameters=lambda: [MagicMock(numel=lambda: 10)]))
        ]
        mock_torch_load.return_value = mock_model

        result = analyze_pytorch_model("model.pt")
        assert result["framework"] == "PyTorch"
        assert result["total_parameters"] == 10
        assert result["layer_distribution"] == {"MagicMock": 1}

def test_analyze_tensorflow_model():
    with patch("tensorflow.keras.models.load_model") as mock_tf_load_model:
        mock_model = MagicMock()
        mock_model.count_params.return_value = 100
        mock_layer = MagicMock()
        type(mock_layer).__name__ = "Dense"
        mock_model.layers = [mock_layer]
        mock_tf_load_model.return_value = mock_model

        result = analyze_tensorflow_model("model.h5")
        assert result["framework"] == "TensorFlow"
        assert result["total_parameters"] == 100
        assert result["layer_distribution"] == {"Dense": 1}

def test_generate_visualization():
    layer_distribution = {"Dense": 10, "Conv2D": 5}
    output_path = "chart.png"
    try:
        generate_visualization(layer_distribution, output_path)
        assert os.path.exists(output_path)
    finally:
        if os.path.exists(output_path):
            os.remove(output_path)
