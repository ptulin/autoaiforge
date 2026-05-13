import pytest
import json
from unittest.mock import patch, MagicMock
from datetime import datetime
from claude_memory_visualizer import fetch_memory_data, filter_memory_data, display_memory_table

def test_fetch_memory_data():
    mock_response = MagicMock()
    mock_response.json.return_value = [{"id": 1, "timestamp": "2023-10-01T12:00:00", "content": "Test memory entry"}]
    mock_response.raise_for_status = MagicMock()

    with patch('requests.get', return_value=mock_response):
        result = fetch_memory_data("http://mockapi.com/memory")
        assert len(result) == 1
        assert result[0]['id'] == 1

def test_filter_memory_data():
    memory_data = [
        {"id": 1, "timestamp": "2023-10-01T12:00:00", "content": "Test memory entry"},
        {"id": 2, "timestamp": "2023-10-02T12:00:00", "content": "Another entry"}
    ]

    # Test filtering by keyword
    result = filter_memory_data(memory_data, keyword="Test")
    assert len(result) == 1
    assert result[0]['id'] == 1

    # Test filtering by timestamp
    since_date = datetime.strptime("2023-10-02", '%Y-%m-%d')
    result = filter_memory_data(memory_data, since=since_date)
    assert len(result) == 1
    assert result[0]['id'] == 2

    # Test filtering with invalid timestamp in data
    memory_data_with_invalid_timestamp = [
        {"id": 3, "timestamp": "invalid-timestamp", "content": "Invalid timestamp entry"}
    ]
    result = filter_memory_data(memory_data_with_invalid_timestamp, since=since_date)
    assert len(result) == 0

def test_display_memory_table():
    memory_data = [
        {"id": 1, "timestamp": "2023-10-01T12:00:00", "content": "Test memory entry"}
    ]
    table = display_memory_table(memory_data)
    assert "Test memory entry" in table
    assert "2023-10-01T12:00:00" in table