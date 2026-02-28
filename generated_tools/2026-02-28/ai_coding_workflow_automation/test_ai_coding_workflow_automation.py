import pytest
import os
import yaml
from unittest.mock import patch, mock_open, MagicMock
from ai_coding_workflow_automation import AIWorkflowAutomation, ConfigError, AIWorkflowHandler

@pytest.fixture
def valid_config():
    return {
        'triggers': [
            {
                'type': 'file_change',
                'file': 'test.py',
                'ai_endpoint': 'http://mock-ai-endpoint.com',
                'instructions': 'Improve this code.',
                'action': 'log'
            }
        ]
    }

def test_load_config_valid(valid_config):
    with patch('os.path.exists', return_value=True):
        with patch('builtins.open', mock_open(read_data=yaml.dump(valid_config))):
            automation = AIWorkflowAutomation('config.yml')
            assert automation.config == valid_config

def test_load_config_invalid():
    with patch('os.path.exists', return_value=True):
        with patch('builtins.open', mock_open(read_data="invalid: yaml: data")):
            with pytest.raises(ConfigError):
                AIWorkflowAutomation('config.yml')

def test_handle_trigger():
    handler = AIWorkflowHandler({
        'triggers': [
            {
                'type': 'file_change',
                'file': 'test.py',
                'ai_endpoint': 'http://mock-ai-endpoint.com',
                'instructions': 'Improve this code.',
                'action': 'log'
            }
        ]
    })

    mock_response = {
        'suggestion': 'Improved code snippet'
    }

    with patch('requests.post') as mock_post:
        mock_post.return_value.json.return_value = mock_response
        mock_post.return_value.raise_for_status = MagicMock()

        with patch('builtins.open', mock_open(read_data="print('hello')")) as mock_file:
            handler.handle_trigger(handler.config['triggers'][0], 'test.py')

        mock_post.assert_called_once_with('http://mock-ai-endpoint.com', json={
            'code': "print('hello')",
            'instructions': 'Improve this code.'
        })
        mock_file.assert_called_once_with('test.py', 'r')