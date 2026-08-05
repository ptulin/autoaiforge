import pytest
from unittest.mock import patch, MagicMock
from agent_behaviour_simulator import simulate_scenario, analyze_performance, visualize_results

@pytest.fixture
def mock_gym_env():
    with patch('gym.Env') as mock_env:
        yield mock_env

def test_simulate_scenario(mock_gym_env):
    scenario = 'my_scenario'
    agent_config = {'agent_id': 1}
    simulation_params = {'scale_factor': 1.0}
    mock_gym_env.return_value.step.return_value = [1, 2, 3]
    performance_metrics = simulate_scenario(scenario, agent_config, simulation_params)
    assert performance_metrics == {0: 1.0, 1: 2.0, 2: 3.0}

def test_analyze_performance():
    results = [1, 2, 3]
    simulation_params = {'scale_factor': 2.0}
    performance_metrics = analyze_performance(results, simulation_params)
    assert performance_metrics == {0: 2.0, 1: 4.0, 2: 6.0}

def test_visualize_results(mock_gym_env):
    results = [1, 2, 3]
    performance_metrics = {0: 1.0, 1: 2.0, 2: 3.0}
    with patch('matplotlib.pyplot.plot') as mock_plot:
        with patch('matplotlib.pyplot.show') as mock_show:
            visualize_results(results, performance_metrics)
            mock_plot.assert_called_once_with(results)
            mock_show.assert_called_once()