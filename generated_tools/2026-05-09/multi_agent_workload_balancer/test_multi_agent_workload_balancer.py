import pytest
import json
from unittest.mock import patch
from multi_agent_workload_balancer import MultiAgentWorkloadBalancer

@pytest.fixture
def sample_config():
    return {
        'agents': [
            {'id': 'agent1', 'name': 'Agent 1'},
            {'id': 'agent2', 'name': 'Agent 2'}
        ],
        'tasks': [
            {'id': 'task1', 'complexity': 1},
            {'id': 'task2', 'complexity': 2}
        ],
        'policy': 'round-robin'
    }

@patch('psutil.cpu_percent', return_value=50)
def test_monitor_agents(mock_cpu, sample_config):
    balancer = MultiAgentWorkloadBalancer(sample_config)
    agent_loads = balancer.monitor_agents()
    assert len(agent_loads) == 2
    assert all(isinstance(load, float) for load in agent_loads.values())

@patch('psutil.cpu_percent', return_value=50)
def test_balance_workload_round_robin(mock_cpu, sample_config):
    balancer = MultiAgentWorkloadBalancer(sample_config)
    assignments = balancer.balance_workload()
    assert len(assignments) == 2
    assert assignments[0]['agent_id'] == 'agent1'
    assert assignments[1]['agent_id'] == 'agent2'

@patch('psutil.cpu_percent', return_value=50)
def test_balance_workload_priority_based(mock_cpu, sample_config):
    sample_config['policy'] = 'priority-based'
    balancer = MultiAgentWorkloadBalancer(sample_config)
    assignments = balancer.balance_workload()
    assert len(assignments) == 2
    assert assignments[0]['agent_id'] == 'agent1'
    assert assignments[1]['agent_id'] == 'agent1'
