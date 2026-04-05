import pytest
from unittest.mock import patch, MagicMock
from ai_dependency_scanner import scan_dependencies, display_report
import subprocess

def test_scan_dependencies_file_not_found():
    result = scan_dependencies("nonexistent_requirements.txt")
    assert result == []

@patch("subprocess.run")
def test_scan_dependencies_success(mock_subprocess):
    mock_subprocess.return_value = MagicMock(
        stdout='[{"name": "tensorflow", "version": "2.6.0", "vulns": [{"id": "CVE-2021-12345", "description": "Sample vulnerability", "fix_version": "2.6.1"}]}]',
        returncode=0
    )
    result = scan_dependencies("requirements.txt")
    assert len(result) == 1
    assert result[0]["name"] == "tensorflow"
    assert result[0]["vulns"][0]["id"] == "CVE-2021-12345"

@patch("subprocess.run")
def test_scan_dependencies_error(mock_subprocess):
    mock_subprocess.side_effect = subprocess.CalledProcessError(1, ["pip-audit"], None)
    result = scan_dependencies("requirements.txt")
    assert result == []

def test_display_report_empty():
    with patch("rich.console.Console.print") as mock_print:
        display_report([])
        mock_print.assert_called_with("[green]No vulnerabilities found![/green]")

def test_display_report_with_data():
    vulnerabilities = [
        {
            "name": "tensorflow",
            "version": "2.6.0",
            "vulns": [
                {
                    "id": "CVE-2021-12345",
                    "description": "Sample vulnerability",
                    "fix_version": "2.6.1",
                }
            ],
        }
    ]
    with patch("rich.console.Console.print") as mock_print:
        display_report(vulnerabilities)
        assert mock_print.called
