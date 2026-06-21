import pytest
import json
import os
from unittest.mock import patch, mock_open
from agentic_ai_scenario_tester import load_scenario, simulate_scenario, generate_report

def test_load_scenario_valid():
    valid_json = '{"scenarios": [{"name": "Test", "goals": ["goal1"], "constraints": ["constraint1"], "environment": {}}]}'
    with patch("builtins.open", mock_open(read_data=valid_json)) as mock_file, \
         patch("os.path.exists", return_value=True):
        data = load_scenario("dummy_path.json")
        assert "scenarios" in data
        assert data["scenarios"][0]["name"] == "Test"

def test_load_scenario_invalid_json():
    invalid_json = '{"scenarios": [{"name": "Test"}]}'
    with patch("builtins.open", mock_open(read_data=invalid_json)) as mock_file, \
         patch("os.path.exists", return_value=True):
        with pytest.raises(ValueError, match="JSON schema validation error"):
            load_scenario("dummy_path.json")

def test_generate_report():
    scenarios = [{"name": "TestScenario", "goals": ["goal1", "goal2"], "constraints": ["constraint1"], "environment": {}}]
    output_dir = "test_output"

    with patch("os.makedirs") as mock_makedirs, \
         patch("pandas.DataFrame.to_csv") as mock_to_csv, \
         patch("builtins.open", mock_open()) as mock_file, \
         patch("matplotlib.pyplot.savefig") as mock_savefig:

        generate_report(scenarios, output_dir)

        mock_makedirs.assert_called_once_with(output_dir, exist_ok=True)
        mock_to_csv.assert_called_once()
        mock_file.assert_called()
        mock_savefig.assert_called()

    if os.path.exists(output_dir):
        os.rmdir(output_dir)

def test_load_scenario_file_not_found():
    with patch("os.path.exists", return_value=False):
        with pytest.raises(FileNotFoundError, match="Scenario file 'dummy_path.json' does not exist."):
            load_scenario("dummy_path.json")