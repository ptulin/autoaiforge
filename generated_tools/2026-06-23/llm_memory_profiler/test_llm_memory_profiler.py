import pytest
from unittest.mock import patch, mock_open, MagicMock
from llm_memory_profiler import profile_memory

def test_profile_memory_file_not_found():
    with pytest.raises(FileNotFoundError):
        profile_memory("non_existent_file.py")

@patch("builtins.open", new_callable=mock_open, read_data="print('Hello World')")
@patch("os.path.isfile", return_value=True)
@patch("psutil.Process")
@patch("tracemalloc.take_snapshot")
def test_profile_memory_basic(mock_snapshot, mock_process, mock_isfile, mock_file):
    mock_process.return_value.memory_info.return_value = type('mem', (object,), {"rss": 100 * 1024 * 1024})()
    mock_snapshot.return_value.statistics.return_value = []

    result = profile_memory("dummy_script.py")

    assert "initial_memory_mb" in result
    assert "peak_memory_mb" in result
    assert result["initial_memory_mb"] == 100.0
    assert result["peak_memory_mb"] == 100.0
    assert result["memory_breakdown"] == []
    assert result["optimization_tips"] == []

@patch("builtins.open", new_callable=mock_open, read_data="print('Hello World')")
@patch("os.path.isfile", return_value=True)
@patch("psutil.Process")
@patch("tracemalloc.take_snapshot")
def test_profile_memory_with_large_allocation(mock_snapshot, mock_process, mock_isfile, mock_file):
    mock_process.return_value.memory_info.side_effect = [
        type('mem', (object,), {"rss": 100 * 1024 * 1024})(),
        type('mem', (object,), {"rss": 1200 * 1024 * 1024})()
    ]
    mock_snapshot.return_value.statistics.return_value = [
        type('stat', (object,), {
            "traceback": [type('frame', (object,), {"filename": "test.py", "lineno": 10})()],
            "size": 15 * 1024 * 1024
        })
    ]

    result = profile_memory("dummy_script.py")

    assert result["initial_memory_mb"] == 100.0
    assert result["peak_memory_mb"] == 1200.0
    assert len(result["memory_breakdown"]) == 1
    assert result["optimization_tips"] == [
        "Consider using smaller batch sizes or model quantization.",
        "Investigate large memory allocations for potential optimizations."
    ]