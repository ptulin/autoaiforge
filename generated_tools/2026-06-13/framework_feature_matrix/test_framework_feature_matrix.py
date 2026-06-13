import pytest
from unittest.mock import patch, MagicMock
from framework_feature_matrix import generate_feature_matrix, save_output
import os
import json

@pytest.fixture
def mock_requests_get():
    with patch("framework_feature_matrix.requests.get") as mock_get:
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = "<html><head><title>Mock Framework</title></head><body></body></html>"
        mock_get.return_value = mock_response
        yield mock_get

def test_generate_feature_matrix_valid_frameworks(mock_requests_get):
    frameworks = ["tensorflow", "pytorch"]
    data = generate_feature_matrix(frameworks)
    assert len(data) == 2
    assert data[0]["Framework"] == "tensorflow"
    assert data[1]["Framework"] == "pytorch"
    assert data[0]["Title"] == "Mock Framework"
    assert data[1]["Title"] == "Mock Framework"

def test_generate_feature_matrix_invalid_framework():
    with pytest.raises(ValueError, match="Framework 'unknown' is not supported."):
        generate_feature_matrix(["unknown"])

def test_save_output_json(tmp_path):
    data = [
        {"Framework": "tensorflow", "Title": "Mock Framework", "URL": "https://www.tensorflow.org/", "Features": "Model Serialization, GPU Support, TPU Support, Built-in Optimizers", "Error": ""}
    ]
    output_file = tmp_path / "output.json"
    save_output(data, "json", output_file)
    with open(output_file, "r") as f:
        saved_data = json.load(f)
    assert saved_data == data

def test_save_output_csv(tmp_path):
    data = [
        {"Framework": "tensorflow", "Title": "Mock Framework", "URL": "https://www.tensorflow.org/", "Features": "Model Serialization, GPU Support, TPU Support, Built-in Optimizers", "Error": ""}
    ]
    output_file = tmp_path / "output.csv"
    save_output(data, "csv", output_file)
    with open(output_file, "r") as f:
        lines = f.readlines()
    assert len(lines) == 2  # Header + 1 data row
    assert "tensorflow" in lines[1]

def test_save_output_markdown(tmp_path):
    data = [
        {"Framework": "tensorflow", "Title": "Mock Framework", "URL": "https://www.tensorflow.org/", "Features": "Model Serialization, GPU Support, TPU Support, Built-in Optimizers", "Error": ""}
    ]
    output_file = tmp_path / "output.md"
    save_output(data, "markdown", output_file)
    with open(output_file, "r") as f:
        content = f.read()
    assert "| Framework   | Title          | URL                         | Features                                                           | Error   |" in content
    assert "| tensorflow  | Mock Framework | https://www.tensorflow.org/ | Model Serialization, GPU Support, TPU Support, Built-in Optimizers |         |" in content