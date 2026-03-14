import pytest
import json
from unittest.mock import patch, mock_open
from cryptography.hazmat.primitives import hashes
from silo_audit_tool import perform_integrity_check, log_access_event, generate_report

def mock_hash(data):
    digest = hashes.Hash(hashes.SHA256())
    digest.update(data)
    return digest.finalize().hex()

def test_perform_integrity_check_success():
    mock_file_content = b"test data"
    expected_checksum = mock_hash(mock_file_content)
    with patch("builtins.open", mock_open(read_data=mock_file_content)):
        with patch("os.path.isfile", return_value=True):
            checksum = perform_integrity_check("test_file.enc")
            assert checksum == expected_checksum

def test_perform_integrity_check_file_not_found():
    with patch("os.path.isfile", return_value=False):
        result = perform_integrity_check("non_existent_file.enc")
        assert result is False

def test_log_access_event():
    event = log_access_event("test_file.enc", success=True)
    assert event == {
        "file": "test_file.enc",
        "access_success": True,
        "event": "access_attempt"
    }

def test_generate_report_json():
    events = [
        {"file": "test_file.enc", "access_success": True, "event": "access_attempt"},
        {"file": "test_file.enc", "integrity_check": "passed", "checksum": "abc123"}
    ]
    report = generate_report(events, "json")
    assert json.loads(report) == events

def test_generate_report_unsupported_format():
    events = []
    report = generate_report(events, "xml")
    assert report is None
