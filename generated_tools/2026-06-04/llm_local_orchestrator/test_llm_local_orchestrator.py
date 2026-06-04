import pytest
from unittest.mock import patch, MagicMock
from llm_local_orchestrator import load_model, run_inference
import torch

def test_load_model():
    with patch('llm_local_orchestrator.AutoTokenizer.from_pretrained') as mock_tokenizer, \
         patch('llm_local_orchestrator.AutoModelForCausalLM.from_pretrained') as mock_model:
        mock_tokenizer.return_value = MagicMock()
        mock_model.return_value = MagicMock()

        model, tokenizer = load_model('./fake_model_path', 'cpu')

        assert model is not None
        assert tokenizer is not None
        mock_tokenizer.assert_called_once_with('./fake_model_path')
        mock_model.assert_called_once_with('./fake_model_path')

def test_run_inference():
    mock_model = MagicMock()
    mock_tokenizer = MagicMock()
    mock_tokenizer.return_tensors = "pt"
    mock_tokenizer.return_value = {
        'input_ids': torch.tensor([[1, 2, 3]]),
        'attention_mask': torch.tensor([[1, 1, 1]])
    }
    mock_model.generate.return_value = torch.tensor([[1, 2, 3]])
    mock_tokenizer.decode.return_value = "decoded text"

    result = run_inference(mock_model, mock_tokenizer, "test input", "cpu", 128)

    assert result == "decoded text"
    mock_tokenizer.assert_called_once_with("test input", return_tensors="pt", padding=True, truncation=True)
    mock_model.generate.assert_called_once()

def test_load_model_failure():
    with patch('llm_local_orchestrator.AutoTokenizer.from_pretrained', side_effect=Exception("Failed")):
        with pytest.raises(RuntimeError, match="Failed to load model: Failed"):
            load_model('./invalid_path', 'cpu')

def test_run_inference_failure():
    mock_model = MagicMock()
    mock_tokenizer = MagicMock()
    mock_tokenizer.return_tensors = "pt"
    mock_tokenizer.return_value = {
        'input_ids': torch.tensor([[1, 2, 3]]),
        'attention_mask': torch.tensor([[1, 1, 1]])
    }
    mock_model.generate.side_effect = Exception("Inference error")

    with pytest.raises(RuntimeError, match="Failed during inference: Inference error"):
        run_inference(mock_model, mock_tokenizer, "test input", "cpu", 128)
