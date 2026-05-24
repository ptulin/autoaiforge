import pytest
import os
import json
from unittest.mock import patch, mock_open
from ai_vuln_scanner import scan_file, scan_directory, generate_report

def test_scan_file():
    mock_code = "def hello():\n    print('Hello, world!')"
    mock_response = {"choices": [{"text": "No vulnerabilities found."}]}

    with patch("builtins.open", mock_open(read_data=mock_code)):
        with patch("openai.Completion.create", return_value=mock_response):
            result = scan_file("test_file.py")
            assert result == "No vulnerabilities found."

def test_scan_directory():
    mock_code = "def hello():\n    print('Hello, world!')"
    mock_response = {"choices": [{"text": "No vulnerabilities found."}]}

    with patch("os.walk", return_value=[("/test", ("subdir",), ("file1.py", "file2.js"))]):
        with patch("builtins.open", mock_open(read_data=mock_code)):
            with patch("openai.Completion.create", return_value=mock_response):
                results = scan_directory("/test")
                assert "/test/file1.py" in results
                assert "/test/file2.js" in results
                assert results["/test/file1.py"] == "No vulnerabilities found."
                assert results["/test/file2.js"] == "No vulnerabilities found."

def test_generate_report(tmp_path):
    results = {
        "file1.py": "No vulnerabilities found.",
        "file2.js": "Potential XSS vulnerability."
    }

    # Test JSON output
    output_file = tmp_path / "report.json"
    generate_report(results, output_file)
    with open(output_file, "r") as f:
        data = json.load(f)
    assert data == results

    # Test console output
    with patch("rich.console.Console.print") as mock_print:
        generate_report(results)
        assert mock_print.called