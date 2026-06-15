import pytest
from unittest.mock import patch, MagicMock
from llm_resource_profiler import profile_resources, generate_report

def test_profile_resources_cpu():
    with patch("llm_resource_profiler.pipeline") as mock_pipeline:
        mock_pipeline.return_value = MagicMock()
        data = profile_resources("dummy_model", "cpu", 1)
        assert "cpu_usage" in data
        assert "ram_usage" in data
        assert len(data["cpu_usage"]) > 0
        assert len(data["ram_usage"]) > 0

def test_profile_resources_gpu():
    with patch("llm_resource_profiler.pipeline") as mock_pipeline, patch("torch.cuda.memory_allocated", return_value=1024):
        mock_pipeline.return_value = MagicMock()
        data = profile_resources("dummy_model", "gpu", 1)
        assert "vram_usage" in data
        assert len(data["vram_usage"]) > 0

def test_generate_report():
    data = {
        "cpu_usage": [10, 20, 30],
        "ram_usage": [1000, 1100, 1200],
        "vram_usage": [200, 300, 400]
    }
    with patch("matplotlib.pyplot.savefig") as mock_savefig:
        generate_report(data, "dummy_output.png")
        mock_savefig.assert_called_once_with("dummy_output.png")