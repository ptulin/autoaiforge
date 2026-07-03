import pytest
from unittest.mock import MagicMock
from agent_simulation_tester import Simulation

def mock_agent(env, logs):
    yield env.timeout(5)
    logs.append({'type': 'agent', 'start_time': 0, 'end_time': 5})

def mock_task(env, logs):
    yield env.timeout(10)
    logs.append({'type': 'task', 'start_time': 0, 'end_time': 10})

def test_simulation_run():
    env_config = {}
    sim = Simulation(env_config)
    sim.add_agent(mock_agent)
    sim.add_task(mock_task)

    sim.run(until=15)

    logs = sim.logs
    assert len(logs) == 2
    assert logs[0]['type'] == 'agent'
    assert logs[1]['type'] == 'task'

def test_simulation_metrics():
    env_config = {}
    sim = Simulation(env_config)
    sim.add_agent(mock_agent)
    sim.add_task(mock_task)

    sim.run(until=15)

    metrics = sim.get_metrics()
    assert len(metrics) == 2
    assert 'completion_time' in metrics.columns
    assert metrics.iloc[0]['completion_time'] == 5

def test_empty_simulation():
    env_config = {}
    sim = Simulation(env_config)
    sim.run(until=10)

    logs = sim.logs
    assert len(logs) == 0

    metrics = sim.get_metrics()
    assert metrics.empty