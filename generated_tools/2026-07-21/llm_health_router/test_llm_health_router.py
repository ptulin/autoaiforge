import pytest
from unittest.mock import patch, MagicMock
import llm_health_router

def mock_requests_get(url, timeout):
    if "health" in url:
        return MagicMock(status_code=200, json=lambda: {
            "latency": 50,
            "uptime": 99.9,
            "cpu_usage": 20,
            "memory_usage": 30
        })
    raise requests.RequestException("Mocked network error")

def mock_requests_post(url, json, timeout):
    if "query" in url:
        return MagicMock(status_code=200, text="Mocked response")
    raise requests.RequestException("Mocked network error")

@patch("llm_health_router.requests.get", side_effect=mock_requests_get)
@patch("llm_health_router.requests.post", side_effect=mock_requests_post)
def test_filter_healthy_instances(mock_get, mock_post):
    instances = [
        {"name": "Instance1", "health_url": "http://instance1/health", "query_url": "http://instance1/query"},
        {"name": "Instance2", "health_url": "http://instance2/health", "query_url": "http://instance2/query"}
    ]
    thresholds = {"latency": 100, "uptime": 95, "cpu_usage": 50, "memory_usage": 50}

    healthy_instances = llm_health_router.filter_healthy_instances(instances, thresholds)
    assert len(healthy_instances) == 2

@patch("llm_health_router.requests.get", side_effect=mock_requests_get)
@patch("llm_health_router.requests.post", side_effect=mock_requests_post)
def test_route_query(mock_get, mock_post):
    instances = [
        {"name": "Instance1", "health_url": "http://instance1/health", "query_url": "http://instance1/query", "latency": 50}
    ]
    query = "Summarize this document"

    response = llm_health_router.route_query(instances, query)
    assert response == "Mocked response"

@patch("llm_health_router.requests.get", side_effect=mock_requests_get)
@patch("llm_health_router.requests.post", side_effect=mock_requests_post)
def test_no_healthy_instances(mock_get, mock_post):
    instances = [
        {"name": "Instance1", "health_url": "http://instance1/health", "query_url": "http://instance1/query"}
    ]
    thresholds = {"latency": 10, "uptime": 95, "cpu_usage": 50, "memory_usage": 50}

    healthy_instances = llm_health_router.filter_healthy_instances(instances, thresholds)
    assert len(healthy_instances) == 0