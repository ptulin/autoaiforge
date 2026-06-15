import pytest
from unittest.mock import mock_open, patch
import pandas as pd
from llm_metrics_log_analyzer import parse_logs, analyze_metrics, save_output


def test_parse_logs():
    log_content = """
    2023-01-01 12:00:00 INFO latency=100 tokens=50 status=success
    2023-01-01 12:01:00 INFO latency=200 tokens=30 status=error
    """
    log_format = r".*latency=(?P<latency>\d+) tokens=(?P<tokens>\d+) status=(?P<status>\w+)"

    with patch("builtins.open", mock_open(read_data=log_content)):
        df = parse_logs("dummy.log", log_format)

    assert not df.empty
    assert len(df) == 2
    assert set(df.columns) == {"latency", "tokens", "status"}


def test_analyze_metrics():
    data = {
        "latency": [100, 200],
        "tokens": [50, 30],
        "status": ["success", "error"]
    }
    df = pd.DataFrame(data)
    metrics = analyze_metrics(df)

    assert metrics["average_latency"] == 150.0
    assert metrics["total_tokens"] == 80
    assert metrics["error_count"] == 1


def test_save_output():
    metrics = {
        "average_latency": 150.0,
        "total_tokens": 80,
        "error_count": 1
    }

    with patch("builtins.open", mock_open()) as mocked_file:
        save_output(metrics, "json", "output.json")
        mocked_file.assert_called_once_with("output.json", "w")

    with patch("pandas.DataFrame.to_csv") as mocked_to_csv:
        save_output(metrics, "csv", "output.csv")
        mocked_to_csv.assert_called_once()

    with patch("builtins.print") as mocked_print:
        save_output(metrics, "console", None)
        mocked_print.assert_called_once()
