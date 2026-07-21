import pytest
from unittest.mock import patch, MagicMock
from ai_traffic_analyzer import analyze_traffic, monitor_interface, analyze_pcap


def test_analyze_traffic_empty():
    packets = []
    result = analyze_traffic(packets)
    assert result == []


def test_analyze_traffic_with_data():
    mock_packet = MagicMock()
    mock_packet.time = 1234567890
    mock_packet.len = 100
    mock_packet[0][1].src = "192.168.1.1"
    mock_packet[0][1].dst = "192.168.1.2"
    mock_packet.haslayer = lambda x: True

    packets = [mock_packet]
    result = analyze_traffic(packets)
    assert isinstance(result, list)


@patch("ai_traffic_analyzer.sniff")
def test_monitor_interface(mock_sniff):
    mock_sniff.return_value = []
    monitor_interface("eth0", None)
    mock_sniff.assert_called_once()


@patch("ai_traffic_analyzer.rdpcap")
def test_analyze_pcap(mock_rdpcap):
    mock_rdpcap.return_value = []
    analyze_pcap("test.pcap", None)
    mock_rdpcap.assert_called_once_with("test.pcap")