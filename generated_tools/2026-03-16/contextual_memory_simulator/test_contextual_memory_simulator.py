import pytest
import numpy as np
from contextual_memory_simulator import MemorySimulator

def test_simulate_basic():
    memory_state = np.array([0.5, 0.5, 0.5])
    new_context = np.array([0.2, 0.3, 0.4])
    result = MemorySimulator.simulate(memory_state, new_context)

    assert "memory_state" in result
    assert "log" in result
    assert result["memory_state"].shape == memory_state.shape

def test_simulate_with_reinforcement():
    memory_state = np.array([0.1, 0.2, 0.3])
    new_context = np.array([0.4, 0.5, 0.6])
    result = MemorySimulator.simulate(memory_state, new_context, reinforcement_factor=2.0)

    expected_memory = np.clip(memory_state * (1 - 0.1) + new_context * 2.0, 0, 1)
    np.testing.assert_array_almost_equal(result["memory_state"], expected_memory)

def test_simulate_with_decay():
    memory_state = np.array([0.9, 0.8, 0.7])
    new_context = np.array([0.1, 0.2, 0.3])
    result = MemorySimulator.simulate(memory_state, new_context, decay_factor=0.5)

    expected_memory = np.clip(memory_state * (1 - 0.5) + new_context, 0, 1)
    np.testing.assert_array_almost_equal(result["memory_state"], expected_memory)

def test_simulate_invalid_shapes():
    memory_state = np.array([0.5, 0.5])
    new_context = np.array([0.2, 0.3, 0.4])

    with pytest.raises(ValueError):
        MemorySimulator.simulate(memory_state, new_context)

def test_simulate_invalid_types():
    memory_state = [0.5, 0.5, 0.5]
    new_context = [0.2, 0.3, 0.4]

    with pytest.raises(ValueError):
        MemorySimulator.simulate(memory_state, new_context)
