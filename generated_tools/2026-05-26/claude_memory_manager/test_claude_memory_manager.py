import pytest
from unittest.mock import patch, MagicMock
from claude_memory_manager import monitor_memory, segment_prompt, interact_with_claude

def test_monitor_memory_below_limit():
    with patch('psutil.virtual_memory') as mock_memory:
        mock_memory.return_value = MagicMock(available=9000 * 1024 ** 2, total=16000 * 1024 ** 2)
        assert monitor_memory(8000) is True

def test_monitor_memory_above_limit():
    with patch('psutil.virtual_memory') as mock_memory:
        mock_memory.return_value = MagicMock(available=7000 * 1024 ** 2, total=16000 * 1024 ** 2)
        assert monitor_memory(8000) is False

def test_segment_prompt():
    prompt = "Line1\nLine2\nLine3\nLine4"
    max_chunk_size = 10
    chunks = segment_prompt(prompt, max_chunk_size)
    assert len(chunks) == 2
    assert chunks[0] == "Line1\nLine2"
    assert chunks[1] == "Line3\nLine4"

def test_interact_with_claude():
    prompt = "Line1\nLine2\nLine3\nLine4"
    max_chunk_size = 10
    with patch('claude_memory_manager.tqdm', lambda x, **kwargs: x):
        responses = interact_with_claude(prompt, max_chunk_size)
        assert len(responses) == 2
        assert responses[0] == "Processed chunk: Line1\nLine2"
        assert responses[1] == "Processed chunk: Line3\nLine4"
