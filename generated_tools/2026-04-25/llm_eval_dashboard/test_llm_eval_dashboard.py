import pytest
import pandas as pd
from unittest.mock import patch, mock_open, MagicMock
from llm_eval_dashboard import load_data, generate_dashboard
import json

def test_load_data_json():
    mock_data = '[{"model": "GPT-5.5", "dataset": "Dataset1", "task": "Task1", "BLEU": 0.8}]'
    with patch("builtins.open", mock_open(read_data=mock_data)):
        df = load_data("test.json")
        assert isinstance(df, pd.DataFrame)
        assert not df.empty
        assert list(df.columns) == ["model", "dataset", "task", "BLEU"]

def test_load_data_csv():
    mock_data = "model,dataset,task,BLEU\nGPT-5.5,Dataset1,Task1,0.8"
    with patch("builtins.open", mock_open(read_data=mock_data)):
        with patch("pandas.read_csv", return_value=pd.read_csv(mock_open(read_data=mock_data)())) as mock_read_csv:
            df = load_data("test.csv")
            mock_read_csv.assert_called_once_with("test.csv")
            assert isinstance(df, pd.DataFrame)
            assert not df.empty
            assert list(df.columns) == ["model", "dataset", "task", "BLEU"]

def test_load_data_invalid_format():
    with pytest.raises(RuntimeError, match="Unsupported file format"):
        load_data("test.txt")

@patch("streamlit.pyplot")
@patch("streamlit.dataframe")
@patch("streamlit.sidebar.multiselect")
@patch("streamlit.title")
def test_generate_dashboard(mock_title, mock_multiselect, mock_dataframe, mock_pyplot):
    mock_multiselect.side_effect = lambda label, options, default: default
    mock_dataframe.return_value = None
    mock_pyplot.return_value = None

    data = pd.DataFrame({
        "model": ["GPT-5.5", "Claude Opus 4.7"],
        "dataset": ["Dataset1", "Dataset2"],
        "task": ["Task1", "Task2"],
        "BLEU": [0.8, 0.9],
        "latency": [1.2, 1.5]
    })

    generate_dashboard(data)

    mock_title.assert_called_once_with("LLM Evaluation Dashboard")
    mock_dataframe.assert_called_once()
    assert mock_pyplot.called
