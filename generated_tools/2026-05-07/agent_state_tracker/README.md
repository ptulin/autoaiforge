# Agent State Tracker

## Description
Agent State Tracker is a lightweight Python library for tracking and managing the state of autonomous AI agents during task execution. It offers state transition management, logging, and checkpointing features for developers building robust AI systems.

## Installation

```bash
pip install pytest==7.4.0
```

## Usage

```python
from agent_state_tracker import State, StateTracker

# Initialize the tracker with an initial state
initial_state = State(name="Idle")
tracker = StateTracker(initial_state)

# Transition to a new state
next_state = State(name="Active")
tracker.transition_to(next_state)

# Checkpoint the current state
tracker.checkpoint()

# Retrieve the state log
print(tracker.get_state_log())
```

## Features
- **State Transition Management**: Validate and manage transitions between states.
- **Checkpointing**: Save the current state for recovery.
- **Built-in Logging**: Log all state changes for debugging and monitoring.

## Example
```python
from agent_state_tracker import State, StateTracker

initial_state = State(name="Idle")
tracker = StateTracker(initial_state)
next_state = State(name="Active")
tracker.transition_to(next_state)
tracker.checkpoint()
print(tracker.get_state_log())
```