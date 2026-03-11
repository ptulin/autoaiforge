import pytest
import json
from unittest.mock import patch, mock_open
from claude_memory_manager import save_memory, retrieve_memory, delete_memory, load_data

def test_save_memory():
    api_url = "http://fakeapi.com"
    api_key = "testkey"
    memory_data = {"key": "value"}

    with patch("requests.post") as mock_post:
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = {"success": True}

        result = save_memory(api_url, api_key, memory_data)
        assert result == {"success": True}
        mock_post.assert_called_once_with(
            f"{api_url}/memory",
            headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
            json=memory_data
        )

def test_retrieve_memory():
    api_url = "http://fakeapi.com"
    api_key = "testkey"

    with patch("requests.get") as mock_get:
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {"memory": []}

        result = retrieve_memory(api_url, api_key)
        assert result == {"memory": []}
        mock_get.assert_called_once_with(
            f"{api_url}/memory",
            headers={"Authorization": f"Bearer {api_key}"}
        )

def test_delete_memory():
    api_url = "http://fakeapi.com"
    api_key = "testkey"
    memory_id = "12345"

    with patch("requests.delete") as mock_delete:
        mock_delete.return_value.status_code = 200
        mock_delete.return_value.json.return_value = {"deleted": True}

        result = delete_memory(api_url, api_key, memory_id)
        assert result == {"deleted": True}
        mock_delete.assert_called_once_with(
            f"{api_url}/memory/{memory_id}",
            headers={"Authorization": f"Bearer {api_key}"}
        )

def test_load_data_json():
    mock_data = '{"key": "value"}'
    with patch("builtins.open", mock_open(read_data=mock_data)) as mock_file, \
         patch("os.path.exists", return_value=True):
        result = load_data("test.json")
        assert result == {"key": "value"}
        mock_file.assert_called_once_with("test.json", "r")

def test_load_data_yaml():
    mock_data = "key: value"
    with patch("builtins.open", mock_open(read_data=mock_data)) as mock_file, \
         patch("os.path.exists", return_value=True):
        result = load_data("test.yaml")
        assert result == {"key": "value"}
        mock_file.assert_called_once_with("test.yaml", "r")

def test_load_data_file_not_found():
    with patch("os.path.exists", return_value=False):
        with pytest.raises(FileNotFoundError):
            load_data("nonexistent.json")

def test_load_data_invalid_format():
    with patch("os.path.exists", return_value=True), \
         patch("builtins.open", mock_open(read_data="")):
        with pytest.raises(ValueError):
            load_data("test.txt")