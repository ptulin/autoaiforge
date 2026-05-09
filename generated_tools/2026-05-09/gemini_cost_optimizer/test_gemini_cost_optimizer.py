import pytest
from unittest.mock import patch, mock_open
from gemini_cost_optimizer import load_configuration, estimate_cost, optimize_cost

def test_load_configuration_yaml():
    yaml_content = """
    models:
      - name: Model A
        input_size: 1024
        output_frequency: 10
        usage_hours: 5
    """
    with patch("builtins.open", mock_open(read_data=yaml_content)):
        config = load_configuration("config.yaml")
        assert "models" in config
        assert len(config["models"]) == 1
        assert config["models"][0]["name"] == "Model A"

def test_load_configuration_json():
    json_content = '{"models": [{"name": "Model B", "input_size": 2048, "output_frequency": 20, "usage_hours": 10}]}'
    with patch("builtins.open", mock_open(read_data=json_content)):
        config = load_configuration("config.json")
        assert "models" in config
        assert len(config["models"]) == 1
        assert config["models"][0]["name"] == "Model B"

def test_estimate_cost():
    config = {
        "models": [
            {"name": "Model A", "input_size": 1024, "output_frequency": 10, "usage_hours": 5},
            {"name": "Model B", "input_size": 2048, "output_frequency": 20, "usage_hours": 10}
        ]
    }
    recommendations = estimate_cost(config)
    assert len(recommendations) == 2
    assert recommendations[0]["Model"] == "Model A"
    assert "Recommendation" in recommendations[0]

def test_optimize_cost():
    yaml_content = """
    models:
      - name: Model A
        input_size: 1024
        output_frequency: 10
        usage_hours: 5
    """
    with patch("builtins.open", mock_open(read_data=yaml_content)):
        result = optimize_cost("config.yaml")
        assert "Model A" in result
        assert "Total Cost ($)" in result
        assert "Recommendation" in result