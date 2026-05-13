import pytest
from unittest.mock import patch
import claude_memory_manager

def test_query_memory():
    with patch("requests.get") as mock_get:
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {"key": "project_status", "value": "ongoing"}

        result = claude_memory_manager.query_memory("http://api.example.com", "project_status")
        assert result == {"key": "project_status", "value": "ongoing"}

def test_add_memory():
    with patch("requests.post") as mock_post:
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = {"success": True}

        result = claude_memory_manager.add_memory("http://api.example.com", "project_status", "completed")
        assert result == {"success": True}

def test_delete_memory():
    with patch("requests.delete") as mock_delete:
        mock_delete.return_value.status_code = 200
        mock_delete.return_value.json.return_value = {"success": True}

        result = claude_memory_manager.delete_memory("http://api.example.com", "project_status")
        assert result == {"success": True}