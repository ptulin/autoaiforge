import pytest
from unittest.mock import patch, MagicMock
from ide_agent_integrator import start_server
import requests
import os
import yaml

def test_start_server_invalid_config():
    with pytest.raises(FileNotFoundError):
        start_server("non_existent_config.yaml")

def test_start_server_missing_keys(tmp_path):
    config_path = tmp_path / "config.yaml"
    with open(config_path, "w") as f:
        yaml.dump({}, f)

    with pytest.raises(ValueError):
        start_server(str(config_path))

@patch("requests.post")
def test_suggest_endpoint(mock_post, tmp_path):
    mock_post.return_value = MagicMock(status_code=200, json=lambda: {"suggestion": "mocked suggestion"})

    config_path = tmp_path / "config.yaml"
    with open(config_path, "w") as f:
        yaml.dump({"ide": "VSCode", "agent_url": "http://mock-agent"}, f)

    start_server(str(config_path))

    # Simulate a request to the endpoint
    response = requests.post("http://127.0.0.1:5000/suggest", json={"code": "print('hello')"})
    assert response.status_code == 200
    assert response.json() == {"suggestion": "mocked suggestion"}
