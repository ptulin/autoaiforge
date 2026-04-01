import pytest
import json
import os
from unittest.mock import patch, MagicMock
from dynamic_behavior_analyzer import analyze_script

def test_analyze_script_valid():
    with patch("subprocess.Popen") as mock_popen, patch("tracemalloc.take_snapshot") as mock_snapshot:
        # Mock subprocess
        mock_process = MagicMock()
        mock_process.communicate.return_value = ("Output with undercover", "")
        mock_popen.return_value = mock_process

        # Mock memory snapshot
        mock_stat = MagicMock()
        mock_stat.traceback = "traceback"
        mock_stat.size = 1024
        mock_snapshot.return_value.statistics.return_value = [mock_stat]

        # Run analysis
        with open("test_script.py", "w") as f:
            f.write("print('Hello World')")

        report = analyze_script("test_script.py", "test_report.json", ["--test"])

        # Assertions
        assert "undercover" in report["suspicious_patterns"]
        assert len(report["memory_usage"]) > 0
        assert os.path.exists("test_report.json")

        # Cleanup
        os.remove("test_script.py")
        os.remove("test_report.json")

def test_analyze_script_file_not_found():
    with pytest.raises(FileNotFoundError):
        analyze_script("non_existent_script.py", "test_report.json", [])

def test_analyze_script_error_handling():
    with patch("subprocess.Popen", side_effect=Exception("Subprocess error")):
        with open("test_script.py", "w") as f:
            f.write("print('Hello World')")

        report = analyze_script("test_script.py", "test_report.json", [])

        assert "error" in report
        assert report["error"] == "Subprocess error"

        # Cleanup
        os.remove("test_script.py")
        os.remove("test_report.json")