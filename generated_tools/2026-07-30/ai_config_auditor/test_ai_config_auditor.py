import pytest
import os
from unittest.mock import patch, MagicMock
from ai_config_auditor import analyze_configuration, load_configuration

def test_analyze_configuration_success():
    mock_response = MagicMock()
    mock_response.choices = [MagicMock(text="Mocked analysis result.")]

    with patch("openai.Completion.create", return_value=mock_response):
        result = analyze_configuration("key: value", "yaml")
        assert result["success"] is True
        assert "Mocked analysis result." in result["analysis"]

def test_analyze_configuration_failure():
    with patch("openai.Completion.create", side_effect=Exception("API Error")):
        result = analyze_configuration("key: value", "yaml")
        assert result["success"] is False
        assert "API Error" in result["error"]

def test_load_configuration():
    test_file = "test_config.yaml"
    test_content = "key: value"

    with open(test_file, "w") as f:
        f.write(test_content)

    try:
        content, format = load_configuration(test_file)
        assert content == test_content
        assert format == "yaml"
    finally:
        os.remove(test_file)

def test_load_configuration_missing_file():
    with pytest.raises(FileNotFoundError):
        load_configuration("non_existent_file.yaml")

def test_load_configuration_unsupported_format():
    test_file = "test_config.txt"
    test_content = "unsupported content"

    with open(test_file, "w") as f:
        f.write(test_content)

    try:
        with pytest.raises(ValueError):
            load_configuration(test_file)
    finally:
        os.remove(test_file)