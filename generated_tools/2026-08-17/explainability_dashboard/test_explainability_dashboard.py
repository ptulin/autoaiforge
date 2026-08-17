import pytest
from unittest.mock import patch, MagicMock
from explainability_dashboard import load_model, load_dataset, create_dashboard
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd


def test_load_model():
    with patch('pandas.read_pickle') as mock_read_pickle:
        mock_read_pickle.return_value = MagicMock()
        model = load_model('model.pkl')
        assert model is not None


def test_load_dataset():
    with patch('pandas.read_csv') as mock_read_csv:
        mock_read_csv.return_value = MagicMock()
        dataset = load_dataset('dataset.csv')
        assert dataset is not None


def test_create_dashboard():
    with patch('dash.Dash') as mock_dash:
        mock_app = MagicMock()
        mock_app.layout = None
        mock_dash.return_value = mock_app
        model = MagicMock()
        dataset = MagicMock()
        app = create_dashboard(model, dataset)
        assert isinstance(app, type(mock_app))


def test_main():
    with patch('argparse.ArgumentParser') as mock_parser:
        mock_parser.return_value = MagicMock()
        mock_parser.return_value.parse_args.return_value = MagicMock(model='model.pkl', dataset='dataset.csv')
        with patch('explainability_dashboard.load_model') as mock_load_model:
            mock_load_model.return_value = MagicMock()
            with patch('explainability_dashboard.load_dataset') as mock_load_dataset:
                mock_load_dataset.return_value = MagicMock()
                with patch('explainability_dashboard.create_dashboard') as mock_create_dashboard:
                    from explainability_dashboard import main
                    main()
                    assert mock_create_dashboard.called