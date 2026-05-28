import pytest
from unittest.mock import patch, MagicMock
from persistent_agent_memory import AgentMemory
import json

def test_sqlite_backend():
    memory = AgentMemory(backend='sqlite')
    memory.save_state('agent_1', {'mood': 'happy'})
    state = memory.load_state('agent_1')
    assert state == {'mood': 'happy'}
    memory.delete_state('agent_1')
    assert memory.load_state('agent_1') is None

def test_json_backend(tmp_path):
    file_path = tmp_path / "memory.json"
    memory = AgentMemory(backend='json', file_path=file_path)
    memory.save_state('agent_2', {'mood': 'sad'})
    state = memory.load_state('agent_2')
    assert state == {'mood': 'sad'}
    memory.delete_state('agent_2')
    assert memory.load_state('agent_2') is None

@patch('redis.Redis')
def test_redis_backend(mock_redis):
    mock_client = MagicMock()
    mock_redis.return_value = mock_client
    memory = AgentMemory(backend='redis', host='localhost', port=6379)

    memory.save_state('agent_3', {'mood': 'excited'})
    mock_client.set.assert_called_with('agent_3', json.dumps({'mood': 'excited'}))

    mock_client.get.return_value = json.dumps({'mood': 'excited'})
    state = memory.load_state('agent_3')
    assert state == {'mood': 'excited'}

    memory.delete_state('agent_3')
    mock_client.delete.assert_called_with('agent_3')