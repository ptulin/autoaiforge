import pytest
import yaml
from unittest.mock import patch, mock_open
from llm_config_manager import generate_config, validate_config, update_config

def test_generate_config(tmp_path):
    output_path = tmp_path / "config.yaml"
    generate_config("llama_cpp", str(output_path))

    with open(output_path, 'r') as f:
        config = yaml.safe_load(f)

    assert config == {
        "model": "path/to/your/model.bin",
        "learning_rate": 0.001,
        "batch_size": 32
    }

def test_validate_config(tmp_path):
    config_path = tmp_path / "config.yaml"
    valid_config = {
        "model": "path/to/your/model.bin",
        "learning_rate": 0.001,
        "batch_size": 32
    }

    with open(config_path, 'w') as f:
        yaml.dump(valid_config, f)

    validate_config(str(config_path), "llama_cpp")

def test_update_config(tmp_path):
    config_path = tmp_path / "config.yaml"
    initial_config = {
        "model": "path/to/your/model.bin",
        "learning_rate": 0.001,
        "batch_size": 32
    }

    with open(config_path, 'w') as f:
        yaml.dump(initial_config, f)

    updates = {"learning_rate": 0.002, "new_param": "value"}
    update_config(str(config_path), updates)

    with open(config_path, 'r') as f:
        updated_config = yaml.safe_load(f)

    assert updated_config["learning_rate"] == 0.002
    assert updated_config["new_param"] == "value"