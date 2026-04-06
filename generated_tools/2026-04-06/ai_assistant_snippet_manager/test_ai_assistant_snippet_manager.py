import pytest
import sqlite3
from unittest.mock import patch, MagicMock
from ai_assistant_snippet_manager import initialize_db, query_ai, save_snippet, retrieve_snippets

def test_initialize_db():
    conn = initialize_db(':memory:')
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='snippets';")
    assert cursor.fetchone() is not None

def test_save_and_retrieve_snippet():
    conn = initialize_db(':memory:')
    save_snippet(conn, 'Test query', 'Test snippet', 'test,example')
    snippets = retrieve_snippets(conn, 'test')
    assert len(snippets) == 1
    assert snippets[0][1] == 'Test query'
    assert snippets[0][2] == 'Test snippet'
    assert snippets[0][3] == 'test,example'

@patch('ai_assistant_snippet_manager.openai.Completion.create')
def test_query_ai(mock_create):
    mock_create.return_value = MagicMock(choices=[MagicMock(text="Generated code snippet")])
    result = query_ai('fake-api-key', 'Test query')
    assert result == "Generated code snippet"
    mock_create.assert_called_once()
