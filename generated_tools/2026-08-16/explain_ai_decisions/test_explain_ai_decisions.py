import pytest
import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from unittest.mock import patch
from explain_ai_decisions import analyze_model_weights, calculate_feature_importance, generate_explanation_report


def test_analyze_model_weights():
    model = LogisticRegression()
    X = np.random.rand(100, 10)
    y = np.random.randint(0, 2, 100)
    model.fit(X, y)
    weights = analyze_model_weights(model)
    assert isinstance(weights, dict)
    assert 'weights' in weights


def test_calculate_feature_importance():
    model = RandomForestClassifier(n_estimators=10)
    X = np.random.rand(100, 10)
    y = np.random.randint(0, 2, 100)
    model.fit(X, y)
    feature_importances = calculate_feature_importance(model)
    assert isinstance(feature_importances, dict)
    assert 'feature_importances' in feature_importances


def test_generate_explanation_report():
    model = LogisticRegression()
    X = np.random.rand(100, 10)
    y = np.random.randint(0, 2, 100)
    model.fit(X, y)
    input_data = pd.DataFrame(X)
    explanation_report = generate_explanation_report(model, input_data)
    assert isinstance(explanation_report, dict)
    assert 'weights' in explanation_report
    assert 'feature_importances' in explanation_report

    @patch('pandas.read_pickle')
    @patch('pandas.read_csv')
    def test_main(mock_read_csv, mock_read_pickle):
        mock_read_pickle.return_value = model
        mock_read_csv.return_value = input_data
        with patch('sys.stdout') as mock_stdout:
            main()
            mock_stdout.write.assert_called()