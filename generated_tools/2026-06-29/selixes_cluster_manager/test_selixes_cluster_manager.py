import pytest
import json
import yaml
from unittest.mock import patch, mock_open
from selixes_cluster_manager import load_config, load_input_data, distribute_tasks

def test_load_config():
    config_content = {
        "nodes": ["node1", "node2"],
        "model": "gpt2"
    }
    with patch("builtins.open", mock_open(read_data=yaml.dump(config_content))):
        with patch("os.path.exists", return_value=True):
            config = load_config("dummy_config.yaml")
            assert config == config_content

def test_load_input_data():
    input_content = ["Hello world", "How are you?"]
    with patch("builtins.open", mock_open(read_data=json.dumps(input_content))):
        with patch("os.path.exists", return_value=True):
            data = load_input_data("dummy_input.json")
            assert data == input_content

@patch("selixes_cluster_manager.distributed_inference.remote")
@patch("ray.get")
def test_distribute_tasks(mock_ray_get, mock_remote):
    input_data = ["Hello world", "How are you?"]
    cluster_config = {
        "nodes": ["node1", "node2"],
        "model": "gpt2"
    }
    mock_ray_get.return_value = [["Generated text 1"], ["Generated text 2"]]
    results = distribute_tasks(input_data, cluster_config)
    assert results == ["Generated text 1", "Generated text 2"]
