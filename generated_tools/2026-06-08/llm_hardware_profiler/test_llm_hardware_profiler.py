import pytest
from unittest.mock import patch, MagicMock
from llm_hardware_profiler import benchmark_model

def test_benchmark_model_huggingface():
    with patch("llm_hardware_profiler.AutoTokenizer.from_pretrained") as mock_tokenizer, \
         patch("llm_hardware_profiler.AutoModelForCausalLM.from_pretrained") as mock_model, \
         patch("llm_hardware_profiler.psutil.virtual_memory") as mock_memory, \
         patch("llm_hardware_profiler.psutil.cpu_percent") as mock_cpu, \
         patch("llm_hardware_profiler.time.time") as mock_time:

        # Mocking the tokenizer and model
        mock_tokenizer.return_value = MagicMock()
        mock_model.return_value = MagicMock()

        # Mocking memory usage
        mock_memory.side_effect = [MagicMock(used=1000000), MagicMock(used=2000000)]

        # Mocking CPU usage
        mock_cpu.return_value = 10.0

        # Mocking time
        mock_time.side_effect = [1.0, 1.5]

        # Run benchmark
        result = benchmark_model("gpt-2", "huggingface", 8)

        # Assertions
        assert result["model_name"] == "gpt-2"
        assert result["framework"] == "huggingface"
        assert result["batch_size"] == 8
        assert result["latency_seconds"] == 0.5
        assert result["memory_usage_bytes"] == 1000000
        assert result["cpu_usage_percent"] == 10.0

def test_benchmark_model_invalid_framework():
    with pytest.raises(ValueError, match="Currently, only the 'huggingface' framework is supported."):
        benchmark_model("gpt-2", "openllm", 8)

def test_benchmark_model_exception_handling():
    with patch("llm_hardware_profiler.AutoTokenizer.from_pretrained", side_effect=Exception("Mocked error")):
        with pytest.raises(RuntimeError, match="Error during benchmarking: Mocked error"):
            benchmark_model("gpt-2", "huggingface", 8)