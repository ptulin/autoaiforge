import pytest
import json
from unittest.mock import patch, MagicMock
from simulate_ai_behavior import load_config, create_environment, run_simulation

def test_load_config(tmp_path):
    config_data = {
        "action_space": 2,
        "observation_space": {"low": 0, "high": 1, "shape": [1]},
        "initial_state": [0.5],
        "reward_function": "lambda state, action: 1",
        "state_transition": "lambda state, action: state",
        "max_steps": 10
    }
    config_path = tmp_path / "config.json"
    with open(config_path, 'w') as f:
        json.dump(config_data, f)

    loaded_config = load_config(config_path)
    assert loaded_config == config_data

def test_create_environment():
    config = {
        "action_space": 2,
        "observation_space": {"low": 0, "high": 1, "shape": [1]},
        "initial_state": [0.5],
        "reward_function": lambda state, action: 1,
        "state_transition": lambda state, action: state,
        "max_steps": 10
    }
    env = create_environment(config)
    assert env.action_space.n == 2
    assert env.observation_space.shape == (1,)
    assert env.reset() == [0.5]

def test_run_simulation():
    config = {
        "action_space": 2,
        "observation_space": {"low": 0, "high": 1, "shape": [1]},
        "initial_state": [0.5],
        "reward_function": lambda state, action: 1,
        "state_transition": lambda state, action: state,
        "max_steps": 10
    }
    with patch('simulate_ai_behavior.load_config', return_value=config), \
         patch('simulate_ai_behavior.create_environment') as mock_env:
        mock_env_instance = MagicMock()
        mock_env.return_value = mock_env_instance
        mock_env_instance.reset.return_value = [0.5]
        mock_env_instance.step.return_value = ([0.5], 1, False, {})

        run_simulation('dummy_path', visualize=False)

        mock_env.assert_called_once()
        mock_env_instance.reset.assert_called_once()
        assert mock_env_instance.step.call_count == 10