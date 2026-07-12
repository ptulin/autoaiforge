import pytest
from unittest.mock import patch, MagicMock
from mesh_orchestration_helper import parse_nodes, generate_yaml_config, validate_nodes

def test_parse_nodes():
    assert parse_nodes("192.168.1.1:4,192.168.1.2:8") == [
        {'ip': '192.168.1.1', 'gpus': 4},
        {'ip': '192.168.1.2', 'gpus': 8}
    ]
    with pytest.raises(ValueError):
        parse_nodes("192.168.1.1,192.168.1.2:8")

def test_generate_yaml_config():
    nodes = [{'ip': '192.168.1.1', 'gpus': 4}, {'ip': '192.168.1.2', 'gpus': 8}]
    yaml_output = generate_yaml_config(nodes, "gpt3", "train.py")
    assert "model: gpt3" in yaml_output
    assert "script: train.py" in yaml_output
    assert "- ip: 192.168.1.1\n  gpus: 4" in yaml_output
    assert "- ip: 192.168.1.2\n  gpus: 8" in yaml_output

def test_validate_nodes():
    nodes = [{'ip': '192.168.1.1', 'gpus': 4}, {'ip': '192.168.1.2', 'gpus': 8}]
    with patch("paramiko.SSHClient") as mock_ssh:
        mock_instance = MagicMock()
        mock_ssh.return_value = mock_instance
        validate_nodes(nodes)
        assert mock_instance.connect.call_count == 2
        mock_instance.connect.assert_any_call('192.168.1.1', username='root', timeout=5)
        mock_instance.connect.assert_any_call('192.168.1.2', username='root', timeout=5)
        mock_instance.close.assert_called()

    with patch("paramiko.SSHClient") as mock_ssh:
        mock_instance = MagicMock()
        mock_ssh.return_value = mock_instance
        mock_instance.connect.side_effect = Exception("Connection failed")
        with pytest.raises(ConnectionError):
            validate_nodes(nodes)
