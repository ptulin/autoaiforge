import pytest
from unittest.mock import MagicMock
from db_change_audit import AuditLogger
import pandas as pd

def test_execute_safe_query():
    mock_connection = MagicMock()
    mock_connection.begin.return_value.__enter__.return_value.execute.return_value.fetchall.return_value = [(1,)]
    mock_connection.begin.return_value.__enter__.return_value.execute.return_value.keys.return_value = ["id"]

    audit_logger = AuditLogger(mock_connection)
    result = audit_logger.execute_safe("SELECT id FROM users")

    assert isinstance(result, pd.DataFrame)
    assert "id" in result.columns
    assert len(result) == 1

def test_execute_safe_modifications():
    mock_connection = MagicMock()
    mock_connection.begin.return_value.__enter__.return_value.execute.return_value.fetchall.return_value = []
    mock_connection.begin.return_value.__enter__.return_value.execute.return_value.keys.return_value = []

    audit_logger = AuditLogger(mock_connection)
    audit_logger.execute_safe("UPDATE users SET age = age + 1")

    assert "modifications" in audit_logger.audit_logs[-1]

def test_export_logs():
    mock_connection = MagicMock()
    audit_logger = AuditLogger(mock_connection)

    audit_logger.audit_logs = [{"query": "SELECT * FROM users"}]
    audit_logger.export_logs("test_logs.json")

    with open("test_logs.json", "r") as f:
        logs = f.read()

    assert "SELECT * FROM users" in logs