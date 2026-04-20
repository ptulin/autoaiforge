import pytest
import json
import pandas as pd
from unittest.mock import patch, MagicMock
from ai_model_benchmark import load_dataset, evaluate_model_responses, generate_report

def test_load_dataset_json():
    dataset = '[{"prompt": "What is AI?", "reference": "Artificial Intelligence is the simulation of human intelligence."}]'
    with patch("builtins.open", new_callable=MagicMock) as mock_open:
        mock_open.return_value.__enter__.return_value.read.return_value = dataset
        result = load_dataset("test.json")
        assert len(result) == 1
        assert result[0]['prompt'] == "What is AI?"

def test_load_dataset_csv():
    dataset = "prompt,reference\nWhat is AI?,Artificial Intelligence is the simulation of human intelligence."
    with patch("pandas.read_csv", return_value=pd.DataFrame([{"prompt": "What is AI?", "reference": "Artificial Intelligence is the simulation of human intelligence."}])):
        result = load_dataset("test.csv")
        assert len(result) == 1
        assert result[0]['prompt'] == "What is AI?"

def test_evaluate_model_responses():
    prompts = [{"prompt": "What is AI?", "reference": "Artificial Intelligence is the simulation of human intelligence."}]
    mock_response = "Artificial Intelligence is the simulation of human intelligence."

    def mock_generate_response(prompt):
        return mock_response

    metrics = evaluate_model_responses(prompts, "GPT-5", mock_generate_response)
    assert len(metrics) == 1
    assert metrics[0]['response'] == mock_response
    assert metrics[0]['bleu_score'] == 1.0

def test_generate_report_json(tmp_path):
    metrics = [{"prompt": "What is AI?", "response": "Artificial Intelligence is the simulation of human intelligence.", "latency": 0.1, "response_length": 50, "bleu_score": 1.0}]
    output_file = tmp_path / "report.json"
    generate_report(metrics, metrics, str(output_file))
    with open(output_file, "r") as f:
        report = json.load(f)
    assert "GPT-5" in report
    assert "Claude-4.7" in report

def test_generate_report_html(tmp_path):
    metrics = [{"prompt": "What is AI?", "response": "Artificial Intelligence is the simulation of human intelligence.", "latency": 0.1, "response_length": 50, "bleu_score": 1.0}]
    output_file = tmp_path / "report.html"
    generate_report(metrics, metrics, str(output_file))
    with open(output_file, "r") as f:
        content = f.read()
    assert "<html>" in content
    assert "GPT-5" in content
    assert "Claude-4.7" in content
