import pytest
import pandas as pd
from unittest.mock import patch, mock_open
from llm_burnout_tracker import analyze_logs, generate_visualization
import os

def test_analyze_logs_empty():
    data = pd.DataFrame()
    result = analyze_logs(data)
    assert result['risk_score'] == 0
    assert "No data provided to analyze." in result['recommendations']

def test_analyze_logs_prolonged_sessions():
    data = pd.DataFrame({
        'timestamp': [
            '2023-01-01 10:00:00',
            '2023-01-01 12:30:00',
            '2023-01-01 15:00:00'
        ],
        'query': ['query1', 'query2', 'query3']
    })
    result = analyze_logs(data)
    assert result['risk_score'] > 0
    assert "Consider taking breaks during long sessions." in result['recommendations']

def test_generate_visualization():
    data = pd.DataFrame({
        'timestamp': [
            '2023-01-01 10:00:00',
            '2023-01-01 10:15:00',
            '2023-01-01 11:00:00'
        ],
        'query': ['query1', 'query2', 'query3']
    })
    with patch("matplotlib.pyplot.savefig") as mock_savefig:
        generate_visualization(data, "test_output.png")
        mock_savefig.assert_called_once_with("test_output.png")
