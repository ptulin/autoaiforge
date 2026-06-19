import pytest
import json
from unittest.mock import patch, MagicMock
from llm_coordinator import load_config, execute_workflow

def test_load_config_valid_file(tmp_path):
    config_data = {"steps": [{"name": "step1", "model": "text-davinci-003", "task": "Summarize this text.", "api_key": "test_key"}]}
    config_file = tmp_path / "config.json"
    config_file.write_text(json.dumps(config_data))

    result = load_config(str(config_file))
    assert result == config_data

def test_load_config_invalid_file():
    with pytest.raises(FileNotFoundError):
        load_config("non_existent_file.json")

def test_execute_workflow():
    config = {
        "steps": [
            {"name": "step1", "model": "text-davinci-003", "task": "Summarize this text.", "api_key": "test_key"}
        ]
    }

    mock_chain = MagicMock()
    mock_chain.run.return_value = "This is a summary."

    with patch("llm_coordinator.OpenAI") as mock_openai:
        mock_openai.return_value = MagicMock()
        with patch("llm_coordinator.LLMChain", return_value=mock_chain):
            results = execute_workflow(config)

    assert results == {"step1": "This is a summary."}

def test_execute_workflow_missing_fields():
    config = {
        "steps": [
            {"name": "step1", "model": "text-davinci-003", "task": "Summarize this text."}
        ]
    }

    results = execute_workflow(config)
    assert results == {"step1": None}
