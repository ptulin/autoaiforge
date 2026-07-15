import pytest
from unittest.mock import patch, MagicMock, ANY
from scapy.all import IP
from live_threat_monitor import load_ai_model, process_packet, monitor_traffic

@patch('live_threat_monitor.load_model')
def test_load_ai_model(mock_load_model):
    mock_load_model.return_value = MagicMock()
    model = load_ai_model("dummy_model_path")
    assert model is not None
    mock_load_model.assert_called_once_with("dummy_model_path")

@patch('live_threat_monitor.sniff')
def test_monitor_traffic(mock_sniff):
    mock_sniff.return_value = None
    model = MagicMock()
    monitor_traffic("eth0", model, None)
    mock_sniff.assert_called_once_with(iface="eth0", prn=ANY, store=False)

@patch('live_threat_monitor.open', create=True)
def test_process_packet(mock_open):
    mock_open.return_value.__enter__.return_value = MagicMock()
    packet = MagicMock()
    packet.__contains__.side_effect = lambda x: x == IP  # Simulate IP in packet
    packet[IP].src = "192.168.1.1"
    packet[IP].dst = "192.168.1.2"
    model = MagicMock()
    model.predict.return_value = [[0.6]]  # Simulate anomaly
    process_packet(packet, model, "log.json")
    model.predict.assert_called_once()
    mock_open.assert_called_once_with("log.json", 'a')