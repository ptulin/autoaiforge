import pytest
from unittest.mock import patch, MagicMock
from claude_usage_monitor import fetch_usage, monitor_usage, generate_report

def test_fetch_usage():
    with patch("requests.get") as mock_get:
        mock_response = MagicMock()
        mock_response.json.return_value = {"requests_per_minute": 50, "usage_limit": 100}
        mock_response.status_code = 200
        mock_get.return_value = mock_response

        result = fetch_usage("fake_api_key")
        assert result == {"requests_per_minute": 50, "usage_limit": 100}

def test_monitor_usage():
    with patch("claude_usage_monitor.fetch_usage") as mock_fetch:
        mock_fetch.return_value = {"requests_per_minute": 90, "usage_limit": 100}
        with patch("time.sleep", return_value=None):
            monitor_usage("fake_api_key", alert_threshold=80, max_iterations=2)
            assert mock_fetch.call_count == 2

def test_generate_report():
    with patch("claude_usage_monitor.fetch_usage") as mock_fetch:
        mock_fetch.return_value = {"requests_per_minute": 50, "usage_limit": 100}
        with patch("time.sleep", return_value=None):
            with patch("pandas.DataFrame.to_csv") as mock_to_csv:
                with patch("matplotlib.pyplot.savefig") as mock_savefig:
                    generate_report("fake_api_key", time_range=2, output_file="test_report.csv")
                    assert mock_fetch.call_count == 2
                    mock_to_csv.assert_called_once_with("test_report.csv", index=False)
                    mock_savefig.assert_called_once_with("test_report.png")
