import pytest
from unittest.mock import patch, MagicMock
import pandas as pd
import torch
from model_comparison_benchmarker import load_dataset, evaluate_model, benchmark

def test_load_dataset():
    data = pd.DataFrame({"text": ["sample1", "sample2"], "label": [0, 1]})
    with patch("pandas.read_csv", return_value=data):
        dataset = load_dataset("dummy_path.csv")
        assert not dataset.empty
        assert "text" in dataset.columns
        assert "label" in dataset.columns

def test_evaluate_model():
    dataset = pd.DataFrame({"text": ["sample1", "sample2"], "label": [0, 1]})
    with patch("transformers.AutoTokenizer.from_pretrained") as mock_tokenizer, \
         patch("transformers.AutoModelForSequenceClassification.from_pretrained") as mock_model:
        
        mock_tokenizer_instance = MagicMock()
        mock_tokenizer_instance.return_value = {
            "input_ids": torch.tensor([[1, 2, 3], [4, 5, 6]]),
            "attention_mask": torch.tensor([[1, 1, 1], [1, 1, 1]])
        }
        mock_tokenizer.return_value = mock_tokenizer_instance

        mock_model_instance = MagicMock()
        mock_model_instance(**MagicMock()).logits = torch.tensor([[0.9, 0.1], [0.1, 0.9]])
        mock_model.return_value = mock_model_instance

        result = evaluate_model("bert-base", dataset, batch_size=16)
        assert "latency" in result
        assert "accuracy" in result
        assert "memory_usage" in result
        assert result["accuracy"] == 1.0

def test_benchmark():
    dataset = pd.DataFrame({"text": ["sample1", "sample2"], "label": [0, 1]})
    with patch("model_comparison_benchmarker.load_dataset", return_value=dataset), \
         patch("model_comparison_benchmarker.evaluate_model", return_value={"latency": 0.1, "accuracy": 1.0, "memory_usage": 0}):
        
        results = benchmark(["bert-base"], ["dummy_path.csv"], batch_size=16)
        assert "bert-base" in results
        assert "dummy_path.csv" in results["bert-base"]
        assert results["bert-base"]["dummy_path.csv"]["accuracy"] == 1.0