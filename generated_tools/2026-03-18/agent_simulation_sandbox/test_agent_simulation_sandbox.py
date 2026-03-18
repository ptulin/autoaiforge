import pytest
from unittest.mock import patch, MagicMock, mock_open
import json
from agent_simulation_sandbox import load_agent, load_scenario, run_simulation

def test_load_agent():
    mock_agent_path = "mock_agent.py"
    with patch("os.path.exists", return_value=True):
        with patch("importlib.util.spec_from_file_location") as mock_spec:
            mock_loader = MagicMock()
            mock_loader.exec_module = MagicMock()
            mock_spec.return_value = MagicMock(loader=mock_loader)
            mock_module = MagicMock()
            mock_module.Agent = MagicMock()
            with patch("sys.modules", {"agent": mock_module}):
                agent = load_agent(mock_agent_path)
                assert isinstance(agent, MagicMock)

def test_load_scenario():
    mock_config_path = "scenario.json"
    mock_scenario = {"environment": "CartPole-v1", "max_steps": 500}
    with patch("os.path.exists", return_value=True):
        with patch("builtins.open", mock_open(read_data=json.dumps(mock_scenario))):
            scenario = load_scenario(mock_config_path)
            assert scenario == mock_scenario

def test_run_simulation():
    mock_agent = MagicMock()
    mock_agent.act.return_value = 0
    mock_env = MagicMock()
    mock_env.reset.return_value = [0.0]
    mock_env.step.return_value = ([0.0], 1, False, {})
    mock_env.close = MagicMock()

    with patch("gym.make", return_value=mock_env):
        total_reward, steps = run_simulation(mock_agent, "CartPole-v1", 10)
        assert total_reward == 10
        assert steps == 10
