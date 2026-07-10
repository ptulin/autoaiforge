import pytest
from unittest.mock import patch
from adaptive_llm_optimizer import profile_hardware, adjust_settings, monitor_performance, optimize_model


def test_profile_hardware():
    with patch("psutil.cpu_count", return_value=8), \
         patch("psutil.virtual_memory", return_value=type("vmem", (object,), {"total": 16 * 1024 ** 3})), \
         patch("torch.cuda.is_available", return_value=True), \
         patch("torch.cuda.get_device_name", return_value="Mock GPU"):
        hardware = profile_hardware()
        assert hardware["cpu_count"] == 8
        assert hardware["memory_gb"] == 16
        assert hardware["gpu_available"] is True
        assert hardware["gpu_name"] == "Mock GPU"


def test_adjust_settings():
    hardware_profile = {"cpu_count": 8, "gpu_available": True}
    settings = adjust_settings(hardware_profile, initial_batch_size=32, precision="FP32")
    assert settings["batch_size"] == 32
    assert settings["precision"] == "FP16"
    assert settings["threads"] == 4


def test_monitor_performance():
    model = "MockModel"
    settings = {"batch_size": 32, "precision": "FP16", "threads": 4}
    performance = monitor_performance(model, settings)
    assert performance["latency"] == pytest.approx(1.0 / 32, rel=1e-2)
    assert performance["throughput"] == pytest.approx(32 / (1.0 / 32), rel=1e-2)


def test_optimize_model():
    with patch("adaptive_llm_optimizer.profile_hardware", return_value={
        "cpu_count": 8,
        "memory_gb": 16,
        "gpu_available": True,
        "gpu_name": "Mock GPU"
    }), patch("adaptive_llm_optimizer.monitor_performance", return_value={
        "latency": 0.03,
        "throughput": 1000
    }):
        settings, performance = optimize_model("model.pt", "gpu", 32, "FP32")
        assert settings["batch_size"] == 32
        assert settings["precision"] == "FP16"
        assert settings["threads"] == 4
        assert performance["latency"] == 0.03
        assert performance["throughput"] == 1000
