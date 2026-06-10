import pytest
import numpy as np
from unittest.mock import patch
from misidentification_analyzer import analyze_errors

def test_analyze_errors_basic():
    predictions = [0, 1, 2, 2, 0]
    true_labels = [0, 1, 1, 2, 0]
    result = analyze_errors(predictions, true_labels, output_json=False)

    assert "confusion_matrix" in result
    assert "classification_report" in result
    assert "misclassified_data" in result
    assert len(result["misclassified_data"]["indices"]) == 1

def test_analyze_errors_with_metadata():
    predictions = [0, 1, 2, 2, 0]
    true_labels = [0, 1, 1, 2, 0]
    metadata = [
        {"age": 25, "gender": "M"},
        {"age": 30, "gender": "F"},
        {"age": 22, "gender": "M"},
        {"age": 28, "gender": "F"},
        {"age": 35, "gender": "M"},
    ]

    with patch("misidentification_analyzer.KMeans.fit_predict", return_value=np.array([0, 1, 1])):
        result = analyze_errors(predictions, true_labels, metadata, output_json=False)

    assert "clusters" in result["misclassified_data"]
    assert len(result["misclassified_data"]["clusters"]) == len(result["misclassified_data"]["indices"])

def test_analyze_errors_empty_input():
    predictions = []
    true_labels = []
    result = analyze_errors(predictions, true_labels, output_json=False)

    assert result["confusion_matrix"] == []
    assert result["classification_report"] == {}
    assert result["misclassified_data"] == {"indices": [], "predictions": [], "true_labels": []}
