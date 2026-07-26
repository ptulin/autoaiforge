import pytest
from unittest.mock import MagicMock
import numpy as np
from micro_llm_splitter import split_model

def test_split_model_single_part():
    model = MagicMock()
    model.state_dict.return_value = {
        "layer1.weight": np.random.rand(10, 10).astype(np.float32),
        "layer2.bias": np.random.rand(10).astype(np.float32)
    }

    max_memory = 1000  # Large enough to fit all weights
    result = split_model(model, max_memory)

    assert len(result) == 1
    assert "weights" in result[0]
    assert "metadata" in result[0]
    assert result[0]["metadata"]["part"] == 1

def test_split_model_multiple_parts():
    model = MagicMock()
    model.state_dict.return_value = {
        "layer1.weight": np.random.rand(1000, 1000).astype(np.float32),
        "layer2.bias": np.random.rand(1000).astype(np.float32)
    }

    max_memory = 1  # Force splitting into multiple parts
    result = split_model(model, max_memory)

    assert len(result) > 1
    for sub_model in result:
        assert "weights" in sub_model
        assert "metadata" in sub_model

def test_split_model_invalid_memory():
    model = MagicMock()
    model.state_dict.return_value = {
        "layer1.weight": np.random.rand(10, 10).astype(np.float32),
        "layer2.bias": np.random.rand(10).astype(np.float32)
    }

    with pytest.raises(ValueError):
        split_model(model, -1)

    with pytest.raises(ValueError):
        split_model(model, 0)