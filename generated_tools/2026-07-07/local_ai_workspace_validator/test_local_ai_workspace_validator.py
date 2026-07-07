import pytest
from unittest.mock import patch, mock_open
import os
from local_ai_workspace_validator import validate_dependencies, validate_hardware, validate_endpoints

def test_validate_dependencies():
    with patch('builtins.open', mock_open(read_data='numpy\ntensorflow')):
        with patch('os.path.exists', return_value=True):
            with patch('builtins.__import__', side_effect=lambda name: None if name in ['numpy', 'tensorflow'] else ModuleNotFoundError()):
                result = validate_dependencies('/fake/path')
                assert result['status'] == 'success'
                assert result['message'] == 'All dependencies are installed.'

def test_validate_dependencies_missing():
    with patch('builtins.open', mock_open(read_data='numpy\ntensorflow')):
        with patch('os.path.exists', return_value=True):
            with patch('builtins.__import__', side_effect=ModuleNotFoundError):
                result = validate_dependencies('/fake/path')
                assert result['status'] == 'error'
                assert 'numpy' in result['missing_dependencies']
                assert 'tensorflow' in result['missing_dependencies']

def test_validate_hardware():
    with patch('psutil.cpu_count', return_value=8):
        with patch('psutil.disk_partitions', return_value=[]):
            result = validate_hardware()
            assert result['status'] == 'warning'
            assert result['gpu_available'] is False
            assert result['cpu_cores'] == 8

def test_validate_endpoints():
    with patch('requests.get') as mock_get:
        mock_get.side_effect = [
            type('Response', (object,), {'status_code': 200}),
            type('Response', (object,), {'status_code': 404})
        ]
        result = validate_endpoints()
        assert result['status'] == 'error'
        assert 'https://api.example.com' in result['unreachable_endpoints']
        assert 'http://localhost:5000' not in result['unreachable_endpoints']
