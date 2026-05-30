import pytest
from unittest.mock import patch, MagicMock
from llm_runtime_monitor import monitor
import time

def dummy_model(duration):
    """A dummy model function to simulate workload."""
    start = time.time()
    while time.time() - start < duration:
        sum(i * i for i in range(10000))

def test_monitor_runs_model():
    with patch('llm_runtime_monitor.psutil.cpu_percent', return_value=10.0), \
         patch('llm_runtime_monitor.psutil.virtual_memory', return_value=MagicMock(percent=50.0)), \
         patch('llm_runtime_monitor.plt.show'):
        result = monitor(dummy_model, 1)
        assert result is None

def test_monitor_collects_metrics():
    with patch('llm_runtime_monitor.psutil.cpu_percent', side_effect=[10.0, 20.0, 30.0]), \
         patch('llm_runtime_monitor.psutil.virtual_memory', side_effect=[MagicMock(percent=50.0), MagicMock(percent=60.0), MagicMock(percent=70.0)]), \
         patch('llm_runtime_monitor.plt.show') as mock_plot:
        monitor(dummy_model, 1)
        mock_plot.assert_called_once()

def test_monitor_handles_exceptions():
    def faulty_model():
        raise ValueError("Test exception")

    with patch('llm_runtime_monitor.psutil.cpu_percent', return_value=10.0), \
         patch('llm_runtime_monitor.psutil.virtual_memory', return_value=MagicMock(percent=50.0)), \
         patch('llm_runtime_monitor.plt.show'):
        with pytest.raises(ValueError):
            monitor(faulty_model)
