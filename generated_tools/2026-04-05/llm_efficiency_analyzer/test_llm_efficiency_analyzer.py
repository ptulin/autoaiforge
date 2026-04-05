import pytest
from unittest.mock import patch, MagicMock
from llm_efficiency_analyzer import evaluate_model_performance, generate_report, generate_plot
from pathlib import Path
import json
import os

def test_evaluate_model_performance():
    with patch("llm_efficiency_analyzer.AutoModelForCausalLM.from_pretrained") as mock_model, \
         patch("llm_efficiency_analyzer.AutoTokenizer.from_pretrained") as mock_tokenizer:

        mock_model.return_value = MagicMock()
        mock_tokenizer.return_value = MagicMock()

        dataset_path = Path("test_dataset.jsonl")
        with open(dataset_path, "w") as f:
            f.write(json.dumps({"text": "Sample text."}) + "\n")

        results = evaluate_model_performance("gpt2", dataset_path, (128, 256), (16, 32))

        assert len(results) > 0
        assert all("seq_len" in r and "batch_size" in r and "compute_time" in r and "performance" in r for r in results)

        os.remove(dataset_path)

def test_generate_report():
    results = [
        {"seq_len": 128, "batch_size": 16, "compute_time": 1.28, "performance": 0.5},
        {"seq_len": 256, "batch_size": 32, "compute_time": 2.56, "performance": 0.75}
    ]

    output_path = Path("test_report.csv")
    generate_report(results, output_path)

    assert output_path.exists()
    with open(output_path, "r") as f:
        lines = f.readlines()
        assert len(lines) == 3  # Header + 2 rows

    os.remove(output_path)

def test_generate_plot():
    results = [
        {"seq_len": 128, "batch_size": 16, "compute_time": 1.28, "performance": 0.5},
        {"seq_len": 256, "batch_size": 16, "compute_time": 2.56, "performance": 0.75}
    ]

    output_path = Path("test_plot.png")
    generate_plot(results, output_path)

    assert output_path.exists()
    os.remove(output_path)
