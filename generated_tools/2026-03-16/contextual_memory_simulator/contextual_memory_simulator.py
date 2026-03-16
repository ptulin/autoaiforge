import numpy as np

class MemorySimulator:
    """
    A class to simulate context-sensitive memory systems.
    """

    @staticmethod
    def simulate(memory_state, new_context, reinforcement_factor=1.0, decay_factor=0.1):
        """
        Simulates memory integration with reinforcement and decay.

        Args:
            memory_state (np.ndarray): The initial memory state represented as a numpy array.
            new_context (np.ndarray): The new context data to integrate into memory.
            reinforcement_factor (float): Factor to reinforce the new memory.
            decay_factor (float): Factor to decay old memory.

        Returns:
            dict: Updated memory state and log of the memory process.
        """
        if not isinstance(memory_state, np.ndarray) or not isinstance(new_context, np.ndarray):
            raise ValueError("memory_state and new_context must be numpy arrays.")

        if memory_state.shape != new_context.shape:
            raise ValueError("memory_state and new_context must have the same shape.")

        # Apply decay to the old memory
        decayed_memory = memory_state * (1 - decay_factor)

        # Integrate new context with reinforcement
        updated_memory = decayed_memory + (new_context * reinforcement_factor)

        # Normalize memory values to prevent overflow
        normalized_memory = np.clip(updated_memory, 0, 1)

        log = {
            "decayed_memory": decayed_memory,
            "updated_memory": updated_memory,
            "normalized_memory": normalized_memory
        }

        return {
            "memory_state": normalized_memory,
            "log": log
        }

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Contextual Memory Simulator")
    parser.add_argument("--memory_state", type=str, required=True, help="Initial memory state as a comma-separated list of floats.")
    parser.add_argument("--new_context", type=str, required=True, help="New context data as a comma-separated list of floats.")
    parser.add_argument("--reinforcement_factor", type=float, default=1.0, help="Reinforcement factor for new memory.")
    parser.add_argument("--decay_factor", type=float, default=0.1, help="Decay factor for old memory.")

    args = parser.parse_args()

    try:
        memory_state = np.array([float(x) for x in args.memory_state.split(",")])
        new_context = np.array([float(x) for x in args.new_context.split(",")])

        simulator = MemorySimulator()
        result = simulator.simulate(memory_state, new_context, args.reinforcement_factor, args.decay_factor)

        print("Updated Memory State:", result["memory_state"])
        print("Log:", result["log"])

    except Exception as e:
        print(f"Error: {e}")
