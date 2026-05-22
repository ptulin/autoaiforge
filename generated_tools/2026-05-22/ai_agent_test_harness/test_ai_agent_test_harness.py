import pytest
from unittest.mock import patch, mock_open, MagicMock
import requests
from datetime import datetime
from ai_agent_test_harness import load_test_config, run_test_case, generate_summary_report

def test_load_test_config():
    mock_yaml = """
    test_cases:
      - name: Test Case 1
        endpoint: http://example.com/api
        input:
          key: value
        expected_output:
          result: success
    """
    with patch("builtins.open", mock_open(read_data=mock_yaml)):
        config = load_test_config("test_config.yaml")
        assert "test_cases" in config
        assert config["test_cases"][0]["name"] == "Test Case 1"

def test_run_test_case_success():
    test_case = {
        "endpoint": "http://example.com/api",
        "input": {"key": "value"},
        "expected_output": {"result": "success"}
    }
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"result": "success"}

    with patch("requests.post", return_value=mock_response):
        status, details = run_test_case(test_case)
        assert status is True
        assert details == {"result": "success"}

def test_run_test_case_failure():
    test_case = {
        "endpoint": "http://example.com/api",
        "input": {"key": "value"},
        "expected_output": {"result": "failure"}
    }
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"result": "success"}

    with patch("requests.post", return_value=mock_response):
        status, details = run_test_case(test_case)
        assert status is False
        assert details == {"result": "success"}

def test_generate_summary_report():
    results = {
        "Test Case 1": {"status": True, "details": "All good"},
        "Test Case 2": {"status": False, "details": "Mismatch"}
    }
    with patch("builtins.open", mock_open()) as mocked_file:
        with patch("ai_agent_test_harness.Console.print") as mock_console:
            with patch("ai_agent_test_harness.datetime") as mock_datetime:
                mock_datetime.now.return_value = datetime(2026, 5, 22, 6, 12, 9, 278344)
                mock_datetime.side_effect = lambda *args, **kwargs: datetime(*args, **kwargs)

                generate_summary_report(results, "output.log")
                mocked_file.assert_called_once_with("output.log", "w")
                handle = mocked_file()
                handle.write.assert_any_call("Test Run - 2026-05-22T06:12:09.278344\n")
                handle.write.assert_any_call("=" * 50 + "\n")
                handle.write.assert_any_call("Test Case 1: PASS\n")
                handle.write.assert_any_call("Details: All good\n\n")
                handle.write.assert_any_call("Test Case 2: FAIL\n")
                handle.write.assert_any_call("Details: Mismatch\n\n")
                mock_console.assert_called_once()
