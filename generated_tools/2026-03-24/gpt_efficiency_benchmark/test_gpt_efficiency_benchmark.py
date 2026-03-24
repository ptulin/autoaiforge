import pytest
from unittest.mock import patch, MagicMock
from gpt_efficiency_benchmark import benchmark_model, generate_report

def test_benchmark_model():
    prompts = ["What is AI?", "Explain quantum physics."]
    with patch("openai.ChatCompletion.create") as mock_create:
        mock_create.return_value = MagicMock(choices=[MagicMock(message=MagicMock(content="Response"))])
        results = benchmark_model("gpt-4", prompts)
        assert len(results) == 2
        assert "latency" in results[0]
        assert "memory" in results[0]
        assert "token_count" in results[0]

def test_generate_report():
    results = {
        "gpt-4": [
            {"latency": 0.5, "memory": 100, "token_count": 50},
            {"latency": 0.6, "memory": 110, "token_count": 60}
        ],
        "gpt-5": [
            {"latency": 0.4, "memory": 90, "token_count": 70},
            {"latency": 0.5, "memory": 95, "token_count": 75}
        ]
    }
    generate_report(results, ["gpt-4", "gpt-5"], "test_report.html")
    with open("test_report.html", "r") as f:
        content = f.read()
        assert "Latency Comparison" in content
        assert "Memory Usage Comparison" in content
        assert "Token Throughput Comparison" in content

def test_benchmark_model_error_handling():
    prompts = ["Invalid prompt"]
    with patch("openai.ChatCompletion.create", side_effect=Exception("API Error")):
        results = benchmark_model("gpt-4", prompts)
        assert len(results) == 1
        assert "error" in results[0]