import pytest
from unittest.mock import patch, MagicMock, mock_open
from ai_agent_flow import load_workflow_config, execute_agent, execute_workflow

# Mock OpenAI ChatCompletion
@pytest.fixture
def mock_openai():
    with patch('ai_agent_flow.ChatCompletion') as mock:
        yield mock

def test_load_workflow_config():
    """Test loading a valid YAML configuration file."""
    config_content = """
    agents:
      agent1:
        type: openai
        model: gpt-3.5-turbo
    workflow:
      - name: step1
        agent: agent1
        input: "Hello"
    """
    with patch('builtins.open', mock_open(read_data=config_content)) as mock_file:
        config = load_workflow_config('dummy_path.yaml')
        assert 'agents' in config
        assert 'workflow' in config
        mock_file.assert_called_once_with('dummy_path.yaml', 'r')

def test_execute_agent(mock_openai):
    """Test executing an agent with mocked OpenAI API."""
    mock_openai.create.return_value = {
        'choices': [{'message': {'content': 'Hello, world!'}}]
    }
    agent_config = {
        'type': 'openai',
        'model': 'gpt-3.5-turbo'
    }
    result = execute_agent(agent_config, "Hello")
    assert result == 'Hello, world!'
    mock_openai.create.assert_called_once_with(
        model='gpt-3.5-turbo',
        messages=[{"role": "user", "content": "Hello"}]
    )

def test_execute_workflow(mock_openai):
    """Test executing a full workflow."""
    mock_openai.create.return_value = {
        'choices': [{'message': {'content': 'Processed'}}]
    }
    config = {
        'agents': {
            'agent1': {
                'type': 'openai',
                'model': 'gpt-3.5-turbo'
            }
        },
        'workflow': [
            {
                'name': 'step1',
                'agent': 'agent1',
                'input': 'Input data'
            }
        ]
    }
    results = execute_workflow(config)
    assert results['step1'] == 'Processed'
    mock_openai.create.assert_called_once_with(
        model='gpt-3.5-turbo',
        messages=[{"role": "user", "content": "Input data"}]
    )