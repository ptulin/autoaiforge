import pytest
from unittest.mock import patch, MagicMock
import pandas as pd
from ai_hardware_optimizer import evaluate_model_performance

def test_evaluate_model_performance_cpu():
    with patch("ai_hardware_optimizer.AutoModel.from_pretrained") as mock_model, \
         patch("ai_hardware_optimizer.AutoTokenizer.from_pretrained") as mock_tokenizer:

        mock_model.return_value = MagicMock()
        mock_tokenizer.return_value = MagicMock()

        results = evaluate_model_performance("bert-base-uncased", "cpu", "8GB")

        assert isinstance(results, pd.DataFrame)
        assert not results.empty
        assert "time_ms" in results.columns

def test_evaluate_model_performance_cuda():
    with patch("ai_hardware_optimizer.AutoModel.from_pretrained") as mock_model, \
         patch("ai_hardware_optimizer.AutoTokenizer.from_pretrained") as mock_tokenizer, \
         patch("torch.cuda.is_available", return_value=True):

        mock_model.return_value = MagicMock()
        mock_tokenizer.return_value = MagicMock()

        results = evaluate_model_performance("bert-base-uncased", "cuda", "8GB")

        assert isinstance(results, pd.DataFrame)
        assert not results.empty
        assert "time_ms" in results.columns

def test_evaluate_model_performance_invalid_model():
    with pytest.raises(ValueError):
        evaluate_model_performance("invalid-model", "cpu", "8GB")