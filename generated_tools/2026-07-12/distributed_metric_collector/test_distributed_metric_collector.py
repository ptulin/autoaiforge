import pytest
from unittest.mock import patch, MagicMock
from distributed_metric_collector import Collector
import time

@patch("distributed_metric_collector.psutil.cpu_percent", return_value=50.0)
@patch("distributed_metric_collector.psutil.virtual_memory")
def test_collector_start_stop(mock_virtual_memory, mock_cpu_percent):
    mock_virtual_memory.return_value.percent = 30.0

    collector = Collector(nodes=["node1", "node2"])
    collector.start()
    time.sleep(0.1)  # Reduced sleep time for faster tests
    collector.stop()

    assert len(collector.data["node1"]) > 0
    assert len(collector.data["node2"]) > 0

@patch("distributed_metric_collector.psutil.cpu_percent", return_value=50.0)
@patch("distributed_metric_collector.psutil.virtual_memory")
def test_visualize(mock_virtual_memory, mock_cpu_percent):
    mock_virtual_memory.return_value.percent = 30.0

    collector = Collector(nodes=["node1"])
    collector.start()
    time.sleep(0.1)  # Reduced sleep time for faster tests
    collector.stop()

    collector.visualize()

    assert len(collector.data["node1"]) > 0

@patch("distributed_metric_collector.psutil.cpu_percent", return_value=50.0)
@patch("distributed_metric_collector.psutil.virtual_memory")
def test_custom_metric_hook(mock_virtual_memory, mock_cpu_percent):
    mock_virtual_memory.return_value.percent = 30.0

    def custom_hook():
        return {"custom_metric": 99.0}

    collector = Collector(nodes=["node1"], metric_hooks=[custom_hook])
    collector.start()
    time.sleep(0.1)  # Reduced sleep time for faster tests
    collector.stop()

    assert "custom_metric" in collector.data["node1"][0]
    assert collector.data["node1"][0]["custom_metric"] == 99.0
