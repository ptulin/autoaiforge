import pytest
import json
from unittest.mock import MagicMock, patch
from model_risk_profiler import ModelRiskProfiler

def test_evaluate_edge_cases():
    mock_model = MagicMock()
    mock_model.predict.side_effect = lambda x: [sum(x[0])]  # Mock prediction logic
    profiler = ModelRiskProfiler(mock_model, test_config={"edge_cases": [
        [0, 0, 0],
        [1, 2, 3]
    ]})

    results = profiler.evaluate_edge_cases()
    assert len(results) == 2
    assert results[0]["prediction"] == [0]
    assert results[1]["prediction"] == [6]

def test_evaluate_adversarial_inputs():
    mock_model = MagicMock()
    mock_model.predict.side_effect = lambda x: [sum(x[0])]  # Mock prediction logic
    profiler = ModelRiskProfiler(mock_model, test_config={"adversarial_inputs": [
        [10, -10, 20]
    ]})

    results = profiler.evaluate_adversarial_inputs()
    assert len(results) == 1
    assert results[0]["prediction"] == [20]

def test_generate_risk_profile():
    mock_model = MagicMock()
    mock_model.predict.side_effect = lambda x: [sum(x[0])]  # Mock prediction logic
    profiler = ModelRiskProfiler(mock_model, test_config={"edge_cases": [
        [1, 1, 1]
    ], "adversarial_inputs": [
        [10, -10, 20]
    ]})

    profile = profiler.generate_risk_profile()
    assert "edge_case_evaluation" in profile
    assert "adversarial_input_evaluation" in profile
    assert profile["edge_case_evaluation"][0]["prediction"] == [3]
    assert profile["adversarial_input_evaluation"][0]["prediction"] == [20]
