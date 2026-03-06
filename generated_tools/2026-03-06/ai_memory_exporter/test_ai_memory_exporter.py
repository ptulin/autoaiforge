import pytest
from unittest.mock import patch, Mock
import json
import yaml
from ai_memory_exporter import fetch_memory_data, export_memory_data

def test_fetch_memory_data():
    mock_response = Mock()
    mock_response.json.return_value = {"memory": "test data"}
    mock_response.raise_for_status = Mock()

    with patch("requests.post", return_value=mock_response) as mock_post:
        result = fetch_memory_data("http://example.com/api", "test_api_key", "chatgpt")
        mock_post.assert_called_once_with(
            "http://example.com/api",
            headers={"Authorization": "Bearer test_api_key", "Content-Type": "application/json"},
            json={"model": "chatgpt"}
        )
        assert result == {"memory": "test data"}

def test_export_memory_data_json(tmp_path):
    memory_data = {"memory": "test data"}
    output_file = tmp_path / "memory.json"

    export_memory_data(memory_data, output_file, "json")

    with open(output_file, "r") as f:
        data = json.load(f)

    assert data == memory_data

def test_export_memory_data_yaml(tmp_path):
    memory_data = {"memory": "test data"}
    output_file = tmp_path / "memory.yaml"

    export_memory_data(memory_data, output_file, "yaml")

    with open(output_file, "r") as f:
        data = yaml.safe_load(f)

    assert data == memory_data

def test_export_memory_data_invalid_format():
    memory_data = {"memory": "test data"}

    with pytest.raises(ValueError, match="Unsupported output format: csv"):
        export_memory_data(memory_data, "memory.csv", "csv")