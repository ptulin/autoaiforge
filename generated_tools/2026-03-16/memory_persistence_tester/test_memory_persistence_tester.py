import pytest
from unittest.mock import patch
import numpy as np
from memory_persistence_tester import simulate_memory

def test_simulate_memory_short_term():
    tasks = 10
    decay_rate = 0.1
    strategy = 'short-term'
    recall_accuracy = simulate_memory(tasks, decay_rate, strategy)
    assert len(recall_accuracy) == tasks
    assert all(0 <= acc <= 1 for acc in recall_accuracy)

def test_simulate_memory_long_term():
    tasks = 10
    decay_rate = 0.1
    strategy = 'long-term'
    recall_accuracy = simulate_memory(tasks, decay_rate, strategy)
    assert len(recall_accuracy) == tasks
    assert all(0 <= acc <= 1 for acc in recall_accuracy)

def test_simulate_memory_episodic():
    tasks = 10
    decay_rate = 0.1
    strategy = 'episodic'
    recall_accuracy = simulate_memory(tasks, decay_rate, strategy)
    assert len(recall_accuracy) == tasks
    assert all(0 <= acc <= 1 for acc in recall_accuracy)

def test_invalid_strategy():
    tasks = 10
    decay_rate = 0.1
    strategy = 'invalid'
    with pytest.raises(ValueError):
        simulate_memory(tasks, decay_rate, strategy)