import pytest
from unittest.mock import patch, MagicMock
from llm_prometheus_exporter import fetch_llm_metrics

@patch('llm_prometheus_exporter.requests.get')
def test_fetch_llm_metrics_success(mock_get):
    mock_response = MagicMock()
    mock_response.json.return_value = {
        'token_usage': 100,
        'memory_usage': 2048000,
        'error_count': 0
    }
    mock_response.raise_for_status.return_value = None
    mock_get.return_value = mock_response

    fetch_llm_metrics("http://localhost:8000")

    from llm_prometheus_exporter import latency_gauge, token_usage_gauge, memory_usage_gauge, error_count_gauge
    assert latency_gauge._value.get() > 0
    assert token_usage_gauge._value.get() == 100
    assert memory_usage_gauge._value.get() == 2048000
    assert error_count_gauge._value.get() == 0

@patch('llm_prometheus_exporter.requests.get')
def test_fetch_llm_metrics_error(mock_get):
    import requests
    mock_get.side_effect = requests.RequestException("Connection error")

    fetch_llm_metrics("http://localhost:8000")

    from llm_prometheus_exporter import error_count_gauge
    assert error_count_gauge._value.get() > 0

@patch('llm_prometheus_exporter.requests.get')
def test_fetch_llm_metrics_partial_data(mock_get):
    mock_response = MagicMock()
    mock_response.json.return_value = {
        'token_usage': 50
    }
    mock_response.raise_for_status.return_value = None
    mock_get.return_value = mock_response

    fetch_llm_metrics("http://localhost:8000")

    from llm_prometheus_exporter import token_usage_gauge, memory_usage_gauge, error_count_gauge
    assert token_usage_gauge._value.get() == 50
    assert memory_usage_gauge._value.get() == 0
    assert error_count_gauge._value.get() == 0