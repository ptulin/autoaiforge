import pytest
import requests
from unittest.mock import patch, Mock
from ai_task_syncer import fetch_tasks, analyze_tasks_with_claude, extract_action_items_from_notes

def test_fetch_tasks():
    with patch("requests.get") as mock_get:
        mock_get.return_value = Mock(status_code=200, json=lambda: [{"content": "Task 1"}, {"content": "Task 2"}])
        tasks = fetch_tasks("todoist", "fake_api_key")
        assert len(tasks) == 2
        assert tasks[0]["content"] == "Task 1"

def test_analyze_tasks_with_claude():
    with patch("openai.Completion.create") as mock_openai:
        mock_openai.return_value = Mock(choices=[Mock(text="1. Task A\n2. Task B")])
        suggestions = analyze_tasks_with_claude([{"content": "Task A"}, {"content": "Task B"}], "fake_claude_key")
        assert "Task A" in suggestions
        assert "Task B" in suggestions

def test_extract_action_items_from_notes():
    with patch("openai.Completion.create") as mock_openai:
        mock_openai.return_value = Mock(choices=[Mock(text="Action Item 1\nAction Item 2")])
        action_items = extract_action_items_from_notes("Meeting notes content", "fake_claude_key")
        assert "Action Item 1" in action_items
        assert "Action Item 2" in action_items