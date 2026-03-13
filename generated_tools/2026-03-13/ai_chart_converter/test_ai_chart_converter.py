import pytest
import json
from unittest.mock import patch, mock_open
from ai_chart_converter import load_chart_data, generate_plotly_chart, generate_matplotlib_chart

def test_load_chart_data_valid():
    mock_data = '{"title": "Test Chart", "traces": []}'
    with patch("builtins.open", mock_open(read_data=mock_data)) as mock_file:
        with patch("os.path.exists", return_value=True):
            data = load_chart_data("mock_file.json")
            assert data["title"] == "Test Chart"

def test_load_chart_data_invalid_json():
    mock_data = '{invalid_json}'
    with patch("builtins.open", mock_open(read_data=mock_data)) as mock_file:
        with patch("os.path.exists", return_value=True):
            with pytest.raises(ValueError):
                load_chart_data("mock_file.json")

def test_load_chart_data_file_not_found():
    with patch("os.path.exists", return_value=False):
        with pytest.raises(FileNotFoundError):
            load_chart_data("non_existent_file.json")

@patch("plotly.graph_objects.Figure.write_html")
def test_generate_plotly_chart(mock_write_html):
    data = {
        "title": "Test Chart",
        "traces": [
            {"type": "scatter", "x": [1, 2, 3], "y": [4, 5, 6], "mode": "lines"}
        ]
    }
    generate_plotly_chart(data, "output.html")
    mock_write_html.assert_called_once_with("output.html")

@patch("matplotlib.pyplot.savefig")
def test_generate_matplotlib_chart(mock_savefig):
    data = {
        "title": "Test Chart",
        "traces": [
            {"type": "scatter", "x": [1, 2, 3], "y": [4, 5, 6]}
        ]
    }
    generate_matplotlib_chart(data, "output.png")
    mock_savefig.assert_called_once_with("output.png")