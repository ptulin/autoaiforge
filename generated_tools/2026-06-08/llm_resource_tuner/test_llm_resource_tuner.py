import pytest
from unittest.mock import patch, MagicMock
from llm_resource_tuner import analyze_resources, save_to_yaml

def test_analyze_resources_valid():
    with patch('transformers.AutoModel.from_pretrained') as mock_model, \
         patch('transformers.AutoTokenizer.from_pretrained') as mock_tokenizer:
        mock_model.return_value = MagicMock()
        mock_tokenizer.return_value = MagicMock()

        result = analyze_resources("gpt-3", "8GB")
        assert result["recommended_batch_size"] == 16
        assert result["recommended_precision"] == "fp16"

def test_analyze_resources_invalid_memory():
    with patch('transformers.AutoModel.from_pretrained') as mock_model, \
         patch('transformers.AutoTokenizer.from_pretrained') as mock_tokenizer:
        mock_model.return_value = MagicMock()
        mock_tokenizer.return_value = MagicMock()

        result = analyze_resources("gpt-3", "invalid_memory")
        assert "error" in result
        assert result["error"] == "Invalid GPU memory format. Use format like '8GB'."

def test_analyze_resources_insufficient_memory():
    with patch('transformers.AutoModel.from_pretrained') as mock_model, \
         patch('transformers.AutoTokenizer.from_pretrained') as mock_tokenizer:
        mock_model.return_value = MagicMock()
        mock_tokenizer.return_value = MagicMock()

        result = analyze_resources("gpt-3", "2GB")
        assert "error" in result
        assert result["error"] == "Insufficient GPU memory. Minimum 4GB required."

def test_save_to_yaml(tmp_path):
    data = {"key": "value"}
    output_file = tmp_path / "output.yaml"
    save_to_yaml(data, output_file)

    with open(output_file, "r") as file:
        content = file.read()
        assert "key: value" in content
