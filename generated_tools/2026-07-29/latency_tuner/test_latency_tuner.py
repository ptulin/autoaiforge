import pytest
from unittest.mock import patch, mock_open
import time
from latency_tuner import LatencyTuner

def mock_stage_function():
    time.sleep(0.1)

def test_benchmark_stage():
    tuner = LatencyTuner("dummy_script.py", ["mock_stage"])
    latency = tuner.benchmark_stage("mock_stage", mock_stage_function)
    assert 0.1 <= latency < 0.2

def test_run_benchmark():
    mock_script = """def mock_stage():
    time.sleep(0.1)
"""
    with patch("builtins.open", mock_open(read_data=mock_script)):
        tuner = LatencyTuner("dummy_script.py", ["mock_stage"])
        tuner.script_globals = {"mock_stage": mock_stage_function}
        latencies = tuner.run_benchmark()
        assert "mock_stage" in latencies
        assert 0.1 <= latencies["mock_stage"] < 0.2

def test_suggest_optimizations():
    tuner = LatencyTuner("dummy_script.py", [])
    latencies = {"stage1": 1.5, "stage2": 0.5}
    suggestions = tuner.suggest_optimizations(latencies)
    assert len(suggestions) == 1
    assert "stage1" in suggestions[0]