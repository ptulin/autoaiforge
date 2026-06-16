import pytest
import pandas as pd
from unittest.mock import patch, mock_open
from io import StringIO
from token_usage_visualizer import parse_log_file, generate_line_chart, generate_bar_chart, generate_pie_chart

def test_parse_log_file_valid():
    data = "timestamp,tokens\n2023-01-01 00:00:00,100\n2023-01-01 01:00:00,200"
    with patch("builtins.open", mock_open(read_data=data)):
        df = pd.read_csv(StringIO(data), parse_dates=['timestamp'])
        with patch("pandas.read_csv", return_value=df):
            result = parse_log_file("mock_file.csv")
            assert isinstance(result, pd.DataFrame)
            assert list(result.columns) == ['timestamp', 'tokens']
            assert len(result) == 2

def test_parse_log_file_invalid():
    data = "invalid_column,another_column\nvalue1,value2"
    with patch("builtins.open", mock_open(read_data=data)):
        with patch("pandas.read_csv", side_effect=pd.errors.ParserError("Error parsing CSV")):
            with pytest.raises(ValueError, match="Error reading log file: Error parsing CSV"):
                parse_log_file("mock_file.csv")

@patch("matplotlib.pyplot.show")
def test_generate_line_chart(mock_show):
    data = pd.DataFrame({
        'timestamp': pd.to_datetime(['2023-01-01 00:00:00', '2023-01-01 01:00:00']),
        'tokens': [100, 200]
    })
    generate_line_chart(data)
    mock_show.assert_called_once()

@patch("matplotlib.pyplot.show")
def test_generate_bar_chart(mock_show):
    data = pd.DataFrame({
        'timestamp': pd.to_datetime(['2023-01-01 00:00:00', '2023-01-01 01:00:00']),
        'tokens': [100, 200]
    })
    generate_bar_chart(data)
    mock_show.assert_called_once()

@patch("matplotlib.pyplot.show")
def test_generate_pie_chart(mock_show):
    data = pd.DataFrame({
        'timestamp': pd.to_datetime(['2023-01-01 00:00:00', '2023-01-02 00:00:00']),
        'tokens': [100, 200]
    })
    generate_pie_chart(data)
    mock_show.assert_called_once()
