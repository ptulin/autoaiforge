import pytest
from unittest.mock import patch, mock_open
import pandas as pd
from patient_data_insight_visualizer import load_data, generate_visualizations

def test_load_data_csv():
    mock_csv = "date,value1,value2\n2023-01-01,10,20\n2023-01-02,15,25"
    with patch("builtins.open", mock_open(read_data=mock_csv)):
        with patch("os.path.exists", return_value=True):
            data = load_data("test.csv")
            assert isinstance(data, pd.DataFrame)
            assert data.shape == (2, 3)

def test_load_data_json():
    mock_json = '[{"date": "2023-01-01", "value1": 10, "value2": 20}, {"date": "2023-01-02", "value1": 15, "value2": 25}]'
    with patch("builtins.open", mock_open(read_data=mock_json)):
        with patch("os.path.exists", return_value=True):
            data = load_data("test.json")
            assert isinstance(data, pd.DataFrame)
            assert data.shape == (2, 3)

def test_generate_visualizations_empty_data():
    empty_data = pd.DataFrame()
    with pytest.raises(ValueError, match="Input data is empty"):
        generate_visualizations(empty_data, "output.html")