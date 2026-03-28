import pytest
import os
from unittest.mock import patch, MagicMock, mock_open
from claude_code_sync import ClaudeSyncHandler
import requests

def test_sync_file_with_claude_success():
    handler = ClaudeSyncHandler("./test_dir", "test_api_key")
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"content": "updated content"}

    with patch("builtins.open", mock_open(read_data="original content")) as mock_file:
        with patch("requests.post", return_value=mock_response):
            handler.sync_file_with_claude("./test_dir/test_file.py")

    mock_file.assert_called_with("./test_dir/test_file.py", "w")
    mock_file().write.assert_called_once_with("updated content")

def test_sync_file_with_claude_no_changes():
    handler = ClaudeSyncHandler("./test_dir", "test_api_key")
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"content": None}

    with patch("builtins.open", mock_open(read_data="original content")) as mock_file:
        with patch("requests.post", return_value=mock_response):
            handler.sync_file_with_claude("./test_dir/test_file.py")

    mock_file.assert_called_once_with("./test_dir/test_file.py", "r")
    mock_file().write.assert_not_called()

def test_sync_file_with_claude_network_error():
    handler = ClaudeSyncHandler("./test_dir", "test_api_key")

    with patch("builtins.open", mock_open(read_data="original content")) as mock_file:
        with patch("requests.post", side_effect=requests.exceptions.RequestException("Network error")):
            handler.sync_file_with_claude("./test_dir/test_file.py")

    mock_file.assert_called_once_with("./test_dir/test_file.py", "r")
    mock_file().write.assert_not_called()
