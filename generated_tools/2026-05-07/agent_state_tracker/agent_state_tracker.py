import logging
from dataclasses import dataclass, field
from typing import Any, Dict, Callable

@dataclass
class State:
    name: str
    data: Dict[str, Any] = field(default_factory=dict)

class StateTracker:
    def __init__(self, initial_state: State):
        self.current_state = initial_state
        self.state_log = []
        self.state_log.append(f"Initialized with state: {self.current_state.name}")
        self.logger = logging.getLogger("StateTracker")
        self.logger.setLevel(logging.INFO)
        handler = logging.StreamHandler()
        handler.setFormatter(logging.Formatter('%(asctime)s - %(message)s'))
        self.logger.addHandler(handler)
        self.logger.info(f"Initialized with state: {self.current_state.name}")

    def transition_to(self, next_state: State, validator: Callable[[State, State], bool] = None):
        if validator and not validator(self.current_state, next_state):
            raise ValueError(f"Invalid state transition from {self.current_state.name} to {next_state.name}")
        self.logger.info(f"Transitioning from {self.current_state.name} to {next_state.name}")
        self.state_log.append(f"Transitioned from {self.current_state.name} to {next_state.name}")
        self.current_state = next_state

    def checkpoint(self):
        self.logger.info(f"Checkpointing state: {self.current_state.name}")
        self.state_log.append(f"Checkpointed state: {self.current_state.name}")

    def get_state_log(self):
        return self.state_log

if __name__ == "__main__":
    initial = State(name="Idle")
    tracker = StateTracker(initial)
    next_state = State(name="Active")
    tracker.transition_to(next_state)
    tracker.checkpoint()
    print(tracker.get_state_log())