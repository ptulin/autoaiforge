import pytest
from unittest.mock import patch
from agent_state_tracker import State, StateTracker

def test_initialization():
    initial_state = State(name="Idle")
    tracker = StateTracker(initial_state)
    assert tracker.current_state.name == "Idle"
    assert "Initialized with state: Idle" in tracker.get_state_log()

def test_transition():
    initial_state = State(name="Idle")
    next_state = State(name="Active")
    tracker = StateTracker(initial_state)
    tracker.transition_to(next_state)
    assert tracker.current_state.name == "Active"
    assert "Transitioned from Idle to Active" in tracker.get_state_log()

def test_invalid_transition():
    initial_state = State(name="Idle")
    next_state = State(name="Active")
    tracker = StateTracker(initial_state)
    def validator(current, next):
        return current.name == "Idle" and next.name == "Active"
    tracker.transition_to(next_state, validator=validator)
    with pytest.raises(ValueError):
        tracker.transition_to(State(name="Paused"), validator=validator)

def test_checkpoint():
    initial_state = State(name="Idle")
    tracker = StateTracker(initial_state)
    tracker.checkpoint()
    assert "Checkpointed state: Idle" in tracker.get_state_log()