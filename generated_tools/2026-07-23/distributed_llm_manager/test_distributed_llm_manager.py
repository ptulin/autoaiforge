import pytest
from unittest.mock import patch, MagicMock
import yaml
from distributed_llm_manager import DistributedLLMManager

@pytest.fixture
def mock_config_file(tmp_path):
    config = {
        'ray_address': 'auto',
        'model': {
            'size': 1000,
            'shards': 4
        }
    }
    config_path = tmp_path / "config.yaml"
    with open(config_path, 'w') as f:
        yaml.dump(config, f)
    return config_path

@patch('ray.init')
def test_setup_cluster(mock_ray_init, mock_config_file):
    manager = DistributedLLMManager(mock_config_file)
    manager.setup_cluster()
    mock_ray_init.assert_called_once_with(address='auto')

@patch('concurrent.futures.ThreadPoolExecutor')
@patch('grpc.server')
def test_start_inference_service(mock_grpc_server, mock_executor, mock_config_file):
    mock_executor_instance = MagicMock()
    mock_executor.return_value = mock_executor_instance
    mock_server_instance = MagicMock()
    mock_grpc_server.return_value = mock_server_instance

    manager = DistributedLLMManager(mock_config_file)
    server = manager.start_inference_service()

    mock_executor.assert_called_once_with(max_workers=10)
    mock_grpc_server.assert_called_once_with(mock_executor_instance)
    assert server == mock_server_instance

@patch('ray.init')
def test_partition_model(mock_ray_init, mock_config_file):
    manager = DistributedLLMManager(mock_config_file)
    shard_size = manager.partition_model()
    assert shard_size == 250
