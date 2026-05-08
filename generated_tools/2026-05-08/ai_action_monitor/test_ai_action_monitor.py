import pytest
import json
from unittest.mock import MagicMock, mock_open, patch
from ai_action_monitor import ActionMonitorHandler

def test_process_action_flagged():
    rules = [{'type': 'file', 'operation': 'delete'}]
    log_file = 'output.log'
    handler = ActionMonitorHandler(rules, log_file)

    action = {'type': 'file', 'operation': 'delete', 'details': 'test.txt'}

    with patch('builtins.open', mock_open()) as mocked_file:
        handler.process_action(action)
        mocked_file().write.assert_called_once_with(json.dumps({'action': action, 'flagged': True}) + '\n')

def test_process_action_not_flagged():
    rules = [{'type': 'file', 'operation': 'delete'}]
    log_file = 'output.log'
    handler = ActionMonitorHandler(rules, log_file)

    action = {'type': 'file', 'operation': 'create', 'details': 'test.txt'}

    with patch('builtins.open', mock_open()) as mocked_file:
        handler.process_action(action)
        mocked_file().write.assert_called_once_with(json.dumps({'action': action, 'flagged': False}) + '\n')

def test_on_modified():
    rules = [{'type': 'file', 'operation': 'delete'}]
    log_file = 'output.log'
    handler = ActionMonitorHandler(rules, log_file)

    mock_event = MagicMock()
    mock_event.is_directory = False
    mock_event.src_path = 'test.log'

    log_content = '{"type": "file", "operation": "delete", "details": "test.txt"}\n'

    with patch('builtins.open', mock_open(read_data=log_content)) as mocked_file:
        handler.on_modified(mock_event)
        mocked_file().write.assert_called_once_with(json.dumps({'action': {'type': 'file', 'operation': 'delete', 'details': 'test.txt'}, 'flagged': True}) + '\n')