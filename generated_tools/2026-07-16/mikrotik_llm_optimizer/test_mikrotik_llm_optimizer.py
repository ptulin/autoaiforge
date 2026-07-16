import pytest
from unittest.mock import MagicMock, patch
from mikrotik_llm_optimizer import optimize_router

def test_optimize_router_success():
    with patch('mikrotik_llm_optimizer.RouterOsApiPool') as mock_api_pool:
        mock_api = MagicMock()
        mock_api_pool.return_value.get_api.return_value = mock_api

        optimize_router('192.168.88.1', 'admin', 'admin', '8000,8001', 10000)

        assert mock_api.get_resource.call_count > 0

def test_optimize_router_no_bandwidth():
    with patch('mikrotik_llm_optimizer.RouterOsApiPool') as mock_api_pool:
        mock_api = MagicMock()
        mock_api_pool.return_value.get_api.return_value = mock_api

        optimize_router('192.168.88.1', 'admin', 'admin', '8000,8001', None)

        assert mock_api.get_resource.call_count > 0

def test_optimize_router_connection_error():
    with patch('mikrotik_llm_optimizer.RouterOsApiPool') as mock_api_pool:
        mock_api_pool.side_effect = Exception("Connection failed")

        with pytest.raises(Exception, match="Connection failed"):
            optimize_router('192.168.88.1', 'admin', 'wrongpass', '8000,8001', 10000)