import pytest
from unittest.mock import patch, MagicMock
import torch
from llm_pruner import prune_model


def test_prune_model():
    with patch('transformers.AutoModelForSequenceClassification.from_pretrained') as mock_model:
        mock_model.return_value.named_parameters.return_value = [('param1', torch.tensor([1.0, 2.0], requires_grad=True)), ('param2', torch.tensor([3.0, 4.0], requires_grad=True))]
        model = prune_model('model_path', 0.5)
        params = list(model.named_parameters())
        assert params[0][1].data.tolist() == [0.0, 2.0]


def test_prune_model_zero_ratio():
    with patch('transformers.AutoModelForSequenceClassification.from_pretrained') as mock_model:
        mock_model.return_value.named_parameters.return_value = [('param1', torch.tensor([1.0, 2.0], requires_grad=True)), ('param2', torch.tensor([3.0, 4.0], requires_grad=True))]
        model = prune_model('model_path', 0.0)
        params = list(model.named_parameters())
        assert params[0][1].data.tolist() == [1.0, 2.0]


def test_prune_model_one_ratio():
    with patch('transformers.AutoModelForSequenceClassification.from_pretrained') as mock_model:
        mock_model.return_value.named_parameters.return_value = [('param1', torch.tensor([1.0, 2.0], requires_grad=True)), ('param2', torch.tensor([3.0, 4.0], requires_grad=True))]
        model = prune_model('model_path', 1.0)
        params = list(model.named_parameters())
        assert params[0][1].data.tolist() == [0.0, 0.0]