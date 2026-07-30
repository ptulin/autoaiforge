import pytest
import json
from unittest.mock import patch, mock_open
from agentic_task_simulator import simulate_agents

def test_simulate_agents_success():
    agent_scripts = ["agent1.py", "agent2.py"]
    scenario = {"steps": ["step1", "step2"]}

    with patch("builtins.open", mock_open(read_data=json.dumps(scenario))):
        with patch("os.path.exists", return_value=True):
            result = simulate_agents(agent_scripts, "scenario.json", visualize=False)

    assert "Simulating agent: agent1.py" in result["logs"]
    assert "Executing step: step1" in result["logs"]
    assert result["metrics"]["total_steps"] == 2
    assert result["metrics"]["agents_used"] == 2

def test_simulate_agents_missing_scenario():
    agent_scripts = ["agent1.py"]

    with patch("os.path.exists", side_effect=lambda x: x != "scenario.json"):
        with pytest.raises(FileNotFoundError):
            simulate_agents(agent_scripts, "scenario.json", visualize=False)

def test_simulate_agents_invalid_json():
    agent_scripts = ["agent1.py"]

    with patch("builtins.open", mock_open(read_data="invalid json")):
        with patch("os.path.exists", return_value=True):
            with pytest.raises(ValueError):
                simulate_agents(agent_scripts, "scenario.json", visualize=False)
