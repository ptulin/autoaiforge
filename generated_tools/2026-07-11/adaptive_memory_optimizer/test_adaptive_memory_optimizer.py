import pytest
from unittest.mock import patch, MagicMock
import adaptive_memory_optimizer as amo

def test_apply_optimization_pruning():
    memory_data = [
        {'timestamp': 1, 'rss': 100, 'vms': 200},
        {'timestamp': 2, 'rss': 150, 'vms': 250},
        {'timestamp': 3, 'rss': 200, 'vms': 300},
        {'timestamp': 4, 'rss': 250, 'vms': 350}
    ]
    result = amo.apply_optimization(memory_data, 'pruning')
    assert result == [
        {'timestamp': 1, 'rss': 100, 'vms': 200},
        {'timestamp': 3, 'rss': 200, 'vms': 300}
    ]

def test_compress_memory_data():
    memory_data = [
        {'timestamp': 1, 'rss': 100, 'vms': 200},
        {'timestamp': 2, 'rss': 150, 'vms': 250},
        {'timestamp': 3, 'rss': 200, 'vms': 300},
        {'timestamp': 4, 'rss': 250, 'vms': 350}
    ]
    result = amo.compress_memory_data(memory_data)
    assert len(result) == 2
    assert result[0]['rss'] == 125  # Average of 100 and 150
    assert result[1]['rss'] == 225  # Average of 200 and 250

def test_partition_memory_data():
    memory_data = [
        {'timestamp': 1, 'rss': 100, 'vms': 200},
        {'timestamp': 2, 'rss': 150, 'vms': 250},
        {'timestamp': 3, 'rss': 200, 'vms': 300},
        {'timestamp': 4, 'rss': 250, 'vms': 350}
    ]
    result = amo.partition_memory_data(memory_data)
    assert len(result) == 2
    assert len(result[0]) == 2
    assert len(result[1]) == 2

@patch('os.path.exists', return_value=True)
@patch('psutil.Popen')
def test_adaptive_memory_optimizer(mock_popen, mock_exists):
    mock_process = MagicMock()
    mock_process.is_running.side_effect = [True, True, False]
    mock_process.memory_info.side_effect = [
        MagicMock(rss=100, vms=200),
        MagicMock(rss=150, vms=250)
    ]
    mock_popen.return_value = mock_process

    with patch('builtins.print') as mock_print:
        amo.adaptive_memory_optimizer('dummy_agent.py', 'pruning', None, 1)
        mock_print.assert_any_call("Monitoring memory usage of agent: dummy_agent.py")
        mock_print.assert_any_call("Memory optimization completed successfully.")