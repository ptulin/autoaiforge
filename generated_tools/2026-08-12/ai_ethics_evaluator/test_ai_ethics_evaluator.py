import pytest
import pandas as pd
from unittest.mock import patch
from ai_ethics_evaluator import evaluate_bias, evaluate_fairness, generate_report

@pytest.fixture
def dataset():
    data = {'target': [0, 1, 0, 1, 0]}
    return pd.DataFrame(data)

@pytest.fixture
def predictions():
    data = {'prediction': [0, 1, 0, 1, 0]}
    return pd.DataFrame(data)

def test_evaluate_bias(dataset):
    bias = evaluate_bias(dataset, pd.DataFrame())
    assert bias == 0.6

def test_evaluate_fairness(dataset, predictions):
    fairness = evaluate_fairness(dataset, predictions)
    assert fairness == 1.0

def test_generate_report(dataset, predictions):
    report = generate_report(dataset, predictions)
    assert 'Bias' in report
    assert 'Fairness' in report
