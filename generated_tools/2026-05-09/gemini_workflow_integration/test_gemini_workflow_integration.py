import pytest
from unittest.mock import patch, MagicMock
from pathlib import Path
import json
from gemini_workflow_integration import generate_files, validate_model_version

@patch("gemini_workflow_integration.requests.get")
def test_validate_model_version_valid(mock_get):
    mock_get.return_value = MagicMock(status_code=200, json=lambda: {"valid": True})
    assert validate_model_version("gemini-3") is True

@patch("gemini_workflow_integration.requests.get")
def test_validate_model_version_invalid(mock_get):
    mock_get.return_value = MagicMock(status_code=200, json=lambda: {"valid": False})
    assert validate_model_version("invalid-model") is False

@patch("gemini_workflow_integration.requests.get")
def test_generate_files(mock_get, tmp_path):
    mock_get.return_value = MagicMock(status_code=200, json=lambda: {"valid": True})

    output_dir = tmp_path / "output"
    generate_files("nlp", "gemini-3", output_dir)

    assert (output_dir / "integration.py").exists()
    assert (output_dir / "config.json").exists()

    with open(output_dir / "config.json") as f:
        config = json.load(f)
        assert config["model_version"] == "gemini-3"
        assert config["workflow_type"] == "nlp"
