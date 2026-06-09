import pytest
from unittest.mock import patch
import numpy as np
from memory_decay_simulator import simulate_decay, exponential_decay, linear_decay, plot_decay

def test_exponential_decay():
    time, memory = exponential_decay(rate=0.05, duration=100)
    assert len(time) == 101
    assert len(memory) == 101
    assert memory[0] == 1
    assert memory[-1] < 1

def test_linear_decay():
    time, memory = linear_decay(rate=0.01, duration=100)
    assert len(time) == 101
    assert len(memory) == 101
    assert memory[0] == 1
    assert memory[-1] == 0

def test_simulate_decay():
    time, memory = simulate_decay("exponential", rate=0.05, duration=100)
    assert len(time) == 101
    assert len(memory) == 101

    time, memory = simulate_decay("linear", rate=0.01, duration=100)
    assert len(time) == 101
    assert len(memory) == 101

    with pytest.raises(ValueError):
        simulate_decay("unsupported", rate=0.01, duration=100)

@patch("memory_decay_simulator.plot_decay")
def test_main(mock_plot):
    import argparse
    from memory_decay_simulator import main
    with patch("argparse.ArgumentParser.parse_args", return_value=argparse.Namespace(strategy="exponential", rate=0.05, duration=100)):
        main()
        mock_plot.assert_called_once()
        args, kwargs = mock_plot.call_args
        assert len(args) == 5
        assert args[0].size == 101  # time array
        assert args[1].size == 101  # memory array
        assert args[2] == "exponential"
        assert args[3] == 0.05
        assert args[4] == 100