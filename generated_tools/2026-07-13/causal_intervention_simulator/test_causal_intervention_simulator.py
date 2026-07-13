import pytest
from unittest.mock import patch, MagicMock
import pandas as pd
import torch
from causal_intervention_simulator import load_model, simulate_intervention, save_results_to_csv

def test_load_model():
    with patch("transformers.AutoModelForCausalLM.from_pretrained") as mock_model, \
         patch("transformers.AutoTokenizer.from_pretrained") as mock_tokenizer:
        mock_model.return_value = MagicMock()
        mock_tokenizer.return_value = MagicMock()

        model, tokenizer = load_model("dummy_model_path")

        assert mock_model.called
        assert mock_tokenizer.called
        assert model is not None
        assert tokenizer is not None

def test_simulate_intervention():
    model = MagicMock()
    tokenizer = MagicMock()
    tokenizer.return_tensors = "pt"
    tokenizer.return_value = {"input_ids": torch.tensor([[1, 2, 3]])}

    mock_outputs = MagicMock()
    mock_outputs.logits = torch.tensor([[0.1, 0.2, 0.3]])
    model.return_value = mock_outputs

    with patch.object(model, "__call__", return_value=mock_outputs):
        original_logits, intervened_logits = simulate_intervention(model, tokenizer, "Hello world", ["neuron_45"])

    assert original_logits is not None
    assert intervened_logits is not None
    assert original_logits.shape == intervened_logits.shape

def test_save_results_to_csv(tmp_path):
    original_logits = torch.tensor([[0.1, 0.2, 0.3]])
    intervened_logits = torch.tensor([[0.0, 0.1, 0.2]])
    output_file = tmp_path / "results.csv"

    save_results_to_csv(original_logits.numpy(), intervened_logits.numpy(), output_file)

    df = pd.read_csv(output_file)
    assert "Original Logits" in df.columns
    assert "Intervened Logits" in df.columns
    assert len(df) == len(original_logits.flatten())
