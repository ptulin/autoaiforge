import pytest
import pandas as pd
from unittest.mock import patch, mock_open
from sandbox_behavior_analyzer import analyze_logs, parse_logs, preprocess_logs, detect_anomalies

def test_parse_logs_json():
    mock_data = '[{"action": "login", "duration": 5}, {"action": "logout", "duration": 3}]'
    with patch("builtins.open", mock_open(read_data=mock_data)):
        df = parse_logs("mock_logs.json")
        assert isinstance(df, pd.DataFrame)
        assert len(df) == 2

def test_parse_logs_csv():
    mock_data = "action,duration\nlogin,5\nlogout,3"
    with patch("builtins.open", mock_open(read_data=mock_data)):
        with patch("pandas.read_csv") as mock_read_csv:
            mock_read_csv.return_value = pd.DataFrame({"action": ["login", "logout"], "duration": [5, 3]})
            df = parse_logs("mock_logs.csv")
            assert isinstance(df, pd.DataFrame)
            assert len(df) == 2

def test_analyze_logs():
    mock_data = '[{"action": "login", "duration": 5}, {"action": "logout", "duration": 3}]'
    with patch("builtins.open", mock_open(read_data=mock_data)):
        with patch("sandbox_behavior_analyzer.detect_anomalies") as mock_detect_anomalies:
            mock_detect_anomalies.return_value = pd.DataFrame({"risk_score": [2.5]})
            anomalies = analyze_logs("mock_logs.json")
            assert "risk_score" in anomalies.columns
            assert len(anomalies) == 1