import pytest
import json
from unittest.mock import patch, MagicMock
from gpt_power_profiler import profile_power_usage

def test_profile_power_usage():
    models = ["gpt-4", "gpt-5"]
    prompts = ["Hello, how are you?", "What is the capital of France?"]

    mock_response = MagicMock()
    mock_response.create.return_value = {"choices": [{"message": {"content": "Mock response"}}]}

    with patch("gpt_power_profiler.ChatCompletion", mock_response):
        with patch("gpt_power_profiler.psutil.cpu_percent", return_value=50):
            with patch("gpt_power_profiler.psutil.sensors_battery", return_value=MagicMock(percent=80)):
                results = profile_power_usage(models, prompts)

    assert "gpt-4" in results
    assert "gpt-5" in results
    assert len(results["gpt-4"]["cpu_usage"]) == len(prompts)
    assert results["gpt-4"]["cpu_usage"] == [50, 50]
    assert results["gpt-4"]["power_usage"] == [80, 80]

def test_empty_prompts():
    models = ["gpt-4"]
    prompts = []

    mock_response = MagicMock()
    mock_response.create.return_value = {"choices": [{"message": {"content": "Mock response"}}]}

    with patch("gpt_power_profiler.ChatCompletion", mock_response):
        with patch("gpt_power_profiler.psutil.cpu_percent", return_value=50):
            with patch("gpt_power_profiler.psutil.sensors_battery", return_value=MagicMock(percent=80)):
                results = profile_power_usage(models, prompts)

    assert "gpt-4" in results
    assert results["gpt-4"]["cpu_usage"] == []
    assert results["gpt-4"]["power_usage"] == []

def test_api_error_handling():
    models = ["gpt-4"]
    prompts = ["Hello"]

    mock_response = MagicMock()
    mock_response.create.side_effect = Exception("API error")

    with patch("gpt_power_profiler.ChatCompletion", mock_response):
        with patch("gpt_power_profiler.psutil.cpu_percent", return_value=50):
            with patch("gpt_power_profiler.psutil.sensors_battery", return_value=MagicMock(percent=80)):
                results = profile_power_usage(models, prompts)

    assert "gpt-4" in results
    assert results["gpt-4"]["cpu_usage"] == []
    assert results["gpt-4"]["power_usage"] == []
