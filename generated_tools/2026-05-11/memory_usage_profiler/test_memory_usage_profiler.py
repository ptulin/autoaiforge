import pytest
from unittest.mock import patch, MagicMock
from memory_usage_profiler import profile_memory
import time

def test_profile_memory_basic():
    """Test the memory profiling decorator with a simple function."""
    @profile_memory
    def simple_function():
        data = [i for i in range(1000)]
        return sum(data)

    result = simple_function()
    assert result == sum(range(1000))

def test_profile_memory_with_mock():
    """Test memory profiling with mocked psutil and time."""
    with patch('psutil.Process') as mock_process, patch('time.time', side_effect=[0, 0.1, 0.2, 0.3]):
        mock_memory_info = MagicMock()
        mock_memory_info.rss = 1024 * 1024 * 10  # 10 MB
        mock_process.return_value.memory_info.return_value = mock_memory_info

        @profile_memory
        def mock_function():
            time.sleep(0.3)  # Simulate some processing

        mock_function()

def test_profile_memory_graph_generation():
    """Test if the memory usage graph is generated."""
    import os

    @profile_memory
    def graph_function():
        data = [i for i in range(1000)]
        return sum(data)

    graph_function()
    assert os.path.exists("graph_function_memory_profile.png")
    os.remove("graph_function_memory_profile.png")