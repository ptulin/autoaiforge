import pytest
from unittest.mock import patch, mock_open
import toml
from claude_plugin_deployer import validate_plugin_config, deploy_plugin

def test_validate_plugin_config_valid():
    config_data = """
    [plugin]
    name = "test_plugin"
    version = "1.0.0"
    """
    with patch("builtins.open", mock_open(read_data=config_data)):
        config = validate_plugin_config("dummy_path.toml")
        assert config['plugin']['name'] == "test_plugin"
        assert config['plugin']['version'] == "1.0.0"

def test_validate_plugin_config_invalid():
    config_data = """
    [plugin]
    name = "test_plugin"
    """
    with patch("builtins.open", mock_open(read_data=config_data)):
        with pytest.raises(ValueError, match="Invalid configuration: 'plugin' section or 'version' key missing."):
            validate_plugin_config("dummy_path.toml")

def test_deploy_plugin():
    config_data = """
    [plugin]
    name = "test_plugin"
    version = "1.0.0"
    """
    with patch("builtins.open", mock_open(read_data=config_data)):
        with patch("claude_plugin_deployer.logger.info") as mock_logger:
            deploy_plugin("dummy_path.toml", test=True)
            mock_logger.assert_any_call("Testing plugin 'test_plugin' version '1.0.0'...")
            mock_logger.assert_any_call("Plugin tests passed successfully.")
            mock_logger.assert_any_call("Deploying plugin 'test_plugin' version '1.0.0'...")
            mock_logger.assert_any_call("Plugin deployed successfully.")