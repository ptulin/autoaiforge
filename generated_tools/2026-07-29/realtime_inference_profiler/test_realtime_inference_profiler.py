import pytest
import asyncio
import time
from unittest.mock import Mock, patch
from realtime_inference_profiler import profile, profile_async

@pytest.fixture
def mock_model():
    """A mock model that simulates inference."""
    mock = Mock()
    mock.side_effect = lambda: time.sleep(0.01)
    return mock

@pytest.mark.asyncio
async def test_profile_async_steady(mock_model):
    """Test profiling with a steady workload."""
    with patch('time.time', side_effect=iter(range(100000))):
        metrics = await profile_async(mock_model, 'steady', rate=10, duration=2, workers=2)
        assert len(metrics) == 20
        assert all('latency' in row for row in metrics.to_dict(orient='records'))

@pytest.mark.asyncio
async def test_profile_async_bursty(mock_model):
    """Test profiling with a bursty workload."""
    with patch('time.time', side_effect=iter(range(100000))):
        metrics = await profile_async(mock_model, 'bursty', rate=10, duration=2, workers=2)
        assert len(metrics) > 0
        assert all('latency' in row for row in metrics.to_dict(orient='records'))

@pytest.mark.asyncio
async def test_profile_async_invalid_workload(mock_model):
    """Test profiling with an invalid workload pattern."""
    with pytest.raises(ValueError):
        await profile_async(mock_model, 'invalid', rate=10, duration=2, workers=2)

def test_profile_json_output(mock_model):
    """Test profiling with JSON output."""
    with patch('time.time', side_effect=iter(range(100000))):
        metrics = profile(mock_model, 'steady', rate=10, duration=2, workers=2, output_format='json')
        assert isinstance(metrics, list)
        assert all('latency' in row for row in metrics)

def test_profile_csv_output(mock_model):
    """Test profiling with CSV output."""
    with patch('time.time', side_effect=iter(range(100000))):
        metrics = profile(mock_model, 'steady', rate=10, duration=2, workers=2, output_format='csv')
        assert isinstance(metrics, str)
        assert 'latency' in metrics