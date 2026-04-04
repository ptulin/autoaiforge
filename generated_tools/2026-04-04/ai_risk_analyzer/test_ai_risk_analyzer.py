import pytest
import json
from unittest.mock import patch, MagicMock
from ai_risk_analyzer import run_script_in_sandbox, analyze_risks

def test_run_script_in_sandbox():
    with patch("subprocess.Popen") as mock_popen, patch("psutil.Process") as mock_process:
        mock_proc = MagicMock()
        mock_proc.communicate.return_value = (b"output", b"error")
        mock_proc.pid = 1234
        mock_popen.return_value = mock_proc

        mock_psutil_process = MagicMock()
        mock_psutil_process.open_files.return_value = [MagicMock(path="/tmp/test.txt")]
        mock_psutil_process.connections.return_value = [MagicMock(raddr="127.0.0.1")]
        mock_process.return_value = mock_psutil_process

        result = run_script_in_sandbox("test_script.py")

        assert result["pid"] == 1234
        assert result["stdout"] == "output"
        assert result["stderr"] == "error"
        assert result["open_files"] == ["/tmp/test.txt"]
        assert result["connections"] == ["127.0.0.1"]

def test_analyze_risks_file_access():
    monitored_data = {
        "open_files": ["/tmp/test.txt"],
        "connections": []
    }
    risk_rules = {
        "rules": [
            {"type": "file_access", "match": "test.txt"}
        ]
    }

    flagged_risks = analyze_risks(monitored_data, risk_rules)

    assert len(flagged_risks) == 1
    assert flagged_risks[0]["type"] == "file_access"
    assert flagged_risks[0]["detail"] == "/tmp/test.txt"

def test_analyze_risks_network_access():
    monitored_data = {
        "open_files": [],
        "connections": ["127.0.0.1"]
    }
    risk_rules = {
        "rules": [
            {"type": "network_access", "match": "127.0.0.1"}
        ]
    }

    flagged_risks = analyze_risks(monitored_data, risk_rules)

    assert len(flagged_risks) == 1
    assert flagged_risks[0]["type"] == "network_access"
    assert flagged_risks[0]["detail"] == "127.0.0.1"