import pytest
from unittest.mock import patch, MagicMock
import os
import json
from local_llm_launcher import load_model, parse_config

def test_load_model_success():
    with patch("local_llm_launcher.AutoTokenizer.from_pretrained") as mock_tokenizer, \
         patch("local_llm_launcher.AutoModelForCausalLM.from_pretrained") as mock_model:
        mock_tokenizer.return_value = MagicMock()
        mock_model.return_value = MagicMock()

        model, tokenizer = load_model("gpt-j", "cpu")
        assert model is not None
        assert tokenizer is not None

def test_load_model_failure():
    with patch("local_llm_launcher.AutoTokenizer.from_pretrained", side_effect=Exception("Model not found")):
        with pytest.raises(Exception, match="Model not found"):
            load_model("non-existent-model", "cpu")

def test_parse_config_success(tmp_path):
    config_data = {"key": "value"}
    config_file = tmp_path / "config.json"
    with open(config_file, "w") as f:
        json.dump(config_data, f)

    parsed_config = parse_config(str(config_file))
    assert parsed_config == config_data

def test_parse_config_file_not_found():
    with pytest.raises(FileNotFoundError):
        parse_config("non_existent_config.json")
