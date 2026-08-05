import pytest
from unittest.mock import patch, MagicMock
import pandas as pd
from llm_security_evaluator import evaluate_security, calculate_robustness, calculate_resistance

@patch('llm_security_evaluator.calculate_robustness')
@patch('llm_security_evaluator.calculate_resistance')
def test_evaluate_security(mock_resistance, mock_robustness):
    mock_robustness.return_value = 0.8
    mock_resistance.return_value = 0.9
    report, suggestions = evaluate_security(None)
    assert report.shape == (2, 2)
    assert len(suggestions) == 0

@patch('llm_security_evaluator.calculate_robustness')
@patch('llm_security_evaluator.calculate_resistance')
def test_evaluate_security_low_robustness(mock_resistance, mock_robustness):
    mock_robustness.return_value = 0.6
    mock_resistance.return_value = 0.9
    report, suggestions = evaluate_security(None)
    assert report.shape == (2, 2)
    assert len(suggestions) == 1

@patch('llm_security_evaluator.calculate_robustness')
@patch('llm_security_evaluator.calculate_resistance')
def test_evaluate_security_low_resistance(mock_resistance, mock_robustness):
    mock_robustness.return_value = 0.8
    mock_resistance.return_value = 0.7
    report, suggestions = evaluate_security(None)
    assert report.shape == (2, 2)
    assert len(suggestions) == 1