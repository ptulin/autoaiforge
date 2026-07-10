import pytest
from unittest.mock import patch, MagicMock
from llm_memory_profiler import profile_memory

def test_profile_memory_torch():
    import torch
    
    # Mock a simple PyTorch model
    class MockTorchModel(torch.nn.Module):
        def forward(self, x):
            return x * 2

    model = MockTorchModel()
    input_data = torch.randn(1, 3, 224, 224)

    with patch("psutil.Process") as mock_process:
        mock_process.return_value.memory_info.return_value.rss = 100 * 1024 * 1024
        result = profile_memory(model, input_data)

    assert "initial_memory_mb" in result
    assert "peak_memory_mb" in result
    assert "inference_time_s" in result

def test_profile_memory_tensorflow():
    import tensorflow as tf

    # Mock a simple TensorFlow model
    class MockTFModel(tf.Module):
        @tf.function
        def __call__(self, x):
            return x * 2

    model = MockTFModel()
    input_data = tf.random.normal([1, 224, 224, 3])

    with patch("psutil.Process") as mock_process:
        mock_process.return_value.memory_info.return_value.rss = 100 * 1024 * 1024
        result = profile_memory(model, input_data)

    assert "initial_memory_mb" in result
    assert "peak_memory_mb" in result
    assert "inference_time_s" in result

def test_invalid_model():
    with pytest.raises(ValueError):
        profile_memory("not_a_model", None)