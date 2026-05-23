import pytest
import json
from unittest.mock import patch, mock_open
from claude_api_diff_checker import load_json, generate_diff, export_diff
import requests

def test_load_json_from_file():
    mock_data = '{"key": "value"}'
    with patch("builtins.open", mock_open(read_data=mock_data)):
        with patch("os.path.exists", return_value=True):
            result = load_json("test.json")
            assert result == {"key": "value"}

def test_load_json_from_url():
    mock_data = {"key": "value"}
    with patch("requests.get") as mock_get:
        mock_get.return_value.json.return_value = mock_data
        mock_get.return_value.status_code = 200
        mock_get.return_value.raise_for_status = lambda: None
        result = load_json("http://example.com/api.json")
        assert result == mock_data

def test_generate_diff():
    old_data = {"key1": "value1"}
    new_data = {"key1": "value2", "key2": "value3"}
    diff = generate_diff(old_data, new_data)
    assert "key1" in diff
    assert "key2" in diff

def test_export_diff_json():
    diff = {"key1": ["value1", "value2"]}
    result = export_diff(diff, "json")
    assert json.loads(result) == diff

def test_export_diff_markdown():
    diff = {"key1": ["value1", "value2"]}
    result = export_diff(diff, "markdown")
    assert "# API Diff Report" in result
    assert "```json" in result
    assert "key1" in result

def test_load_json_invalid_file():
    with patch("os.path.exists", return_value=False):
        with pytest.raises(ValueError, match="File not found"):
            load_json("nonexistent.json")

def test_load_json_invalid_url():
    with patch("requests.get") as mock_get:
        mock_get.side_effect = requests.RequestException("Error")
        with pytest.raises(ValueError, match="Failed to fetch JSON from URL"):
            load_json("http://invalid-url.com")