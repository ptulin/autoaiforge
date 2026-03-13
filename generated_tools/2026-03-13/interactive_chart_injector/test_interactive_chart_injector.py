import pytest
from unittest.mock import patch
from interactive_chart_injector import render_chart
from IPython.display import display

def test_render_chart_valid_scatter():
    chart_data = {
        "type": "scatter",
        "data": [
            {"x": [1, 2, 3], "y": [4, 5, 6], "mode": "lines", "name": "Test Line"}
        ],
        "layout": {"title": "Test Scatter Chart"}
    }

    with patch("interactive_chart_injector.display") as mock_display:
        render_chart(chart_data)
        mock_display.assert_called_once()

def test_render_chart_invalid_json():
    invalid_json = "{\"type\": \"scatter\", \"data\": [\"invalid\"]"

    with pytest.raises(ValueError, match="Invalid JSON string provided."):
        render_chart(invalid_json)

def test_render_chart_missing_keys():
    chart_data = {
        "type": "scatter",
        "data": []  # Missing 'layout'
    }

    with pytest.raises(ValueError, match="Input data must contain the keys: {.*}"):
        render_chart(chart_data)

def test_render_chart_unsupported_type():
    chart_data = {
        "type": "pie",
        "data": [
            {"labels": ["A", "B"], "values": [10, 20]}
        ],
        "layout": {"title": "Test Pie Chart"}
    }

    with pytest.raises(ValueError, match="Unsupported chart type: pie"):
        render_chart(chart_data)