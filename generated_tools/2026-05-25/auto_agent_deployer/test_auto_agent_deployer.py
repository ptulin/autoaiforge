import pytest
from unittest.mock import patch, MagicMock, mock_open
import auto_agent_deployer

def test_load_yaml_config():
    mock_yaml_content = """agents: []"""
    with patch('os.path.exists', return_value=True):
        with patch('builtins.open', mock_open(read_data=mock_yaml_content)) as mock_file:
            config = auto_agent_deployer.load_yaml_config('dummy_path.yaml')
            assert config == {'agents': []}
            mock_file.assert_called_once_with('dummy_path.yaml', 'r')

def test_load_yaml_config_file_not_found():
    with patch('os.path.exists', return_value=False):
        with pytest.raises(FileNotFoundError):
            auto_agent_deployer.load_yaml_config('nonexistent.yaml')

def test_deploy_to_aws_lambda():
    agent_config = {
        'name': 'test_agent',
        'runtime': 'python3.8',
        'role': 'arn:aws:iam::123456789012:role/service-role/test-role',
        'handler': 'lambda_function.lambda_handler',
        'code_zip': b'fake-zip-content',
        'description': 'Test Lambda Function',
        'timeout': 10,
        'memory_size': 128
    }

    with patch('boto3.client') as mock_boto_client:
        mock_lambda_client = MagicMock()
        mock_boto_client.return_value = mock_lambda_client
        logger = MagicMock()

        auto_agent_deployer.deploy_to_aws_lambda(agent_config, logger)

        mock_lambda_client.create_function.assert_called_once_with(
            FunctionName='test_agent',
            Runtime='python3.8',
            Role='arn:aws:iam::123456789012:role/service-role/test-role',
            Handler='lambda_function.lambda_handler',
            Code={'ZipFile': b'fake-zip-content'},
            Description='Test Lambda Function',
            Timeout=10,
            MemorySize=128
        )
        logger.info.assert_called_with("Successfully deployed agent 'test_agent' to AWS Lambda.")

def test_deploy_agents_with_unsupported_type():
    config = {
        'agents': [
            {
                'name': 'unsupported_agent',
                'type': 'unsupported_type'
            }
        ]
    }
    logger = MagicMock()

    auto_agent_deployer.deploy_agents(config, logger)

    logger.warning.assert_called_once_with("Unsupported agent type 'unsupported_type' for agent 'unsupported_agent'.")
