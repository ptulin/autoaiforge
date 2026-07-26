import pytest
import torch
from unittest.mock import patch, MagicMock
import os
from llm_micro_optimizer import optimize_model, prune_weights, compress_embeddings

def test_prune_weights():
    model = torch.nn.Linear(10, 5)
    original_weights = model.weight.clone()
    pruned_model = prune_weights(model, 'high')
    assert not torch.equal(original_weights, pruned_model.weight), "Weights should be pruned."

def test_compress_embeddings():
    model = torch.nn.Embedding(10, 5)
    compressed_model = compress_embeddings(model)
    assert model.weight.size() == compressed_model.weight.size(), "Embedding size should remain the same."

def test_optimize_model():
    model = torch.nn.Linear(10, 5)
    temp_model_path = "temp_model.pth"
    optimized_model_path = "optimized_model.pth"

    torch.save(model, temp_model_path)

    with patch("torch.load", return_value=model):
        with patch("torch.save") as mock_save:
            optimize_model(temp_model_path, "high", optimized_model_path)
            mock_save.assert_called_once(), "Model should be saved after optimization."

    if os.path.exists(temp_model_path):
        os.remove(temp_model_path)
    if os.path.exists(optimized_model_path):
        os.remove(optimized_model_path)
