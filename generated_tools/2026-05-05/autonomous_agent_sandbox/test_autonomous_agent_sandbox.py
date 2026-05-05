import pytest
from unittest.mock import patch, MagicMock
import pandas as pd
import json
import yaml
from autonomous_agent_sandbox import load_scenario, load_agent, run_simulation

def test_load_scenario_json(tmp_path):
    scenario_path = tmp_path / "scenario.json"
    scenario_data = {"environment": "CartPole-v1", "episodes": 5}
    scenario_path.write_text(json.dumps(scenario_data))

    result = load_scenario(str(scenario_path))
    assert result == scenario_data

def test_load_scenario_yaml(tmp_path):
    scenario_path = tmp_path / "scenario.yaml"
    scenario_data = {"environment": "CartPole-v1", "episodes": 5}
    scenario_path.write_text(yaml.dump(scenario_data))

    result = load_scenario(str(scenario_path))
    assert result == scenario_data

def test_load_agent(tmp_path):
    agent_path = tmp_path / "agent.py"
    agent_code = """
class Agent:
    def act(self, observation):
        return 0
"""
    agent_path.write_text(agent_code)

    agent_class = load_agent(str(agent_path))
    agent_instance = agent_class()
    assert agent_instance.act(None) == 0

def test_run_simulation():
    scenario = {"environment": "CartPole-v1", "episodes": 1}

    class MockAgent:
        def act(self, observation):
            return 0

    with patch("gym.make") as mock_make:
        mock_env = MagicMock()
        mock_env.reset.return_value = [0, 0, 0, 0]
        mock_env.step.return_value = ([0, 0, 0, 0], 1, True, {})
        mock_make.return_value = mock_env

        results = run_simulation(scenario, MockAgent)
        assert isinstance(results, pd.DataFrame)
        assert len(results) == 1
        assert results.iloc[0]["reward"] == 1
