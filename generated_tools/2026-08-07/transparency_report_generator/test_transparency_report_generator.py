import pytest
import pandas as pd
from unittest.mock import patch, MagicMock
from transparency_report_generator import generate_report
import matplotlib.pyplot as plt
import pickle
import os
from sklearn.ensemble import RandomForestClassifier


def test_generate_report_success(tmp_path):
    # Create a temporary model and dataset
    model_path = tmp_path / 'model.pkl'
    data_path = tmp_path / 'data.csv'
    model = RandomForestClassifier(random_state=42)
    model.n_features_in_ = 10
    data = pd.DataFrame({'feature1': [1, 2, 3], 'feature2': [4, 5, 6], 'target': [0, 1, 0]})
    data.to_csv(data_path, index=False)
    with open(model_path, 'wb') as f:
        pickle.dump(model, f)
    
    # Mock the file operations
    with patch('matplotlib.pyplot.imshow') as mock_imshow:
        mock_imshow.return_value = None
        with patch('matplotlib.pyplot.savefig') as mock_savefig:
            mock_savefig.return_value = None
            with patch('matplotlib.pyplot.colorbar') as mock_colorbar:
                mock_colorbar.return_value = None
                with patch('matplotlib.pyplot.close') as mock_close:
                    mock_close.return_value = None
                    report = generate_report(str(model_path), str(data_path))
                    assert 'Model Complexity' in report
                    assert 'Feature Correlation' in report
                    assert 'Decision Boundary Analysis' in report


def test_generate_report_model_load_failure(tmp_path):
    # Create a temporary dataset
    data_path = tmp_path / 'data.csv'
    data = pd.DataFrame({'feature1': [1, 2, 3], 'feature2': [4, 5, 6], 'target': [0, 1, 0]})
    data.to_csv(data_path, index=False)
    
    # Mock the model load failure
    report = generate_report('non_existent_model.pkl', str(data_path))
    assert 'No such file or directory' in report


def test_generate_report_data_load_failure(tmp_path):
    # Create a temporary model
    model_path = tmp_path / 'model.pkl'
    model = RandomForestClassifier(random_state=42)
    model.n_features_in_ = 10
    with open(model_path, 'wb') as f:
        pickle.dump(model, f)
    
    # Mock the data load failure
    report = generate_report(str(model_path), 'non_existent_data.csv')
    assert 'No such file or directory' in report