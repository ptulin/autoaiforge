import pytest
import pandas as pd
import numpy as np
from unittest.mock import patch, MagicMock
from io import BytesIO
from matplotlib.figure import Figure
from ai_collab_evaluator import evaluate_collaboration

@pytest.fixture
def mock_data():
    data = pd.DataFrame({
        'user_engagement': [0.8, 0.9, 0.7],
        'ai_accuracy': [0.9, 0.8, 0.7],
        'task_completion_rate': [0.7, 0.8, 0.9]
    })
    return data

@patch('pandas.read_csv')
def test_evaluate_collaboration(mock_read_csv, mock_data):
    mock_read_csv.return_value = mock_data
    assert evaluate_collaboration('logs.csv', 'report.pdf') == 'Evaluation report generated successfully'

@patch('pandas.read_csv')
def test_evaluate_collaboration_empty_data(mock_read_csv):
    mock_read_csv.return_value = pd.DataFrame()
    assert evaluate_collaboration('logs.csv', 'report.pdf') == 'No data available for evaluation'

@patch('pandas.read_csv')
@patch('matplotlib.pyplot.savefig')
def test_evaluate_collaboration_save_report(mock_savefig, mock_read_csv, mock_data):
    mock_read_csv.return_value = mock_data
    mock_savefig.side_effect = Exception('Mocked savefig error')
    assert evaluate_collaboration('logs.csv', 'report.pdf') == 'Mocked savefig error'