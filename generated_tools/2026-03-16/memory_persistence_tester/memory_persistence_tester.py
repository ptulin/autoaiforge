import argparse
import numpy as np
import matplotlib.pyplot as plt

def simulate_memory(tasks, decay_rate, strategy):
    """Simulates memory persistence based on the given strategy."""
    np.random.seed(42)  # For reproducibility
    memory = []
    recall_accuracy = []

    for task in range(tasks):
        # Add new memory
        memory.append(np.random.random())

        # Apply decay
        memory = [m * (1 - decay_rate) for m in memory]

        # Retrieval based on strategy
        if strategy == 'short-term':
            retrieved = memory[-1] if memory else 0
        elif strategy == 'long-term':
            retrieved = memory[0] if memory else 0
        elif strategy == 'episodic':
            retrieved = np.mean(memory) if memory else 0
        else:
            raise ValueError(f"Unknown strategy: {strategy}")

        # Simulate recall accuracy
        recall_accuracy.append(retrieved)

    return recall_accuracy

def generate_report(recall_accuracy, tasks, strategy):
    """Generates a graphical report of memory performance."""
    plt.figure(figsize=(10, 6))
    plt.plot(range(tasks), recall_accuracy, label=f"Strategy: {strategy}")
    plt.title("Memory Persistence Performance")
    plt.xlabel("Tasks")
    plt.ylabel("Recall Accuracy")
    plt.legend()
    plt.grid()
    plt.tight_layout()
    plt.show()

def main():
    parser = argparse.ArgumentParser(description="Memory Persistence Tester")
    parser.add_argument('--tasks', type=int, required=True, help="Number of tasks to simulate")
    parser.add_argument('--decay_rate', type=float, required=True, help="Memory decay rate (0-1)")
    parser.add_argument('--strategy', type=str, required=True, choices=['short-term', 'long-term', 'episodic'], help="Memory strategy")
    parser.add_argument('--report', action='store_true', help="Generate graphical report")

    args = parser.parse_args()

    recall_accuracy = simulate_memory(args.tasks, args.decay_rate, args.strategy)

    print(f"Simulation completed for {args.tasks} tasks with strategy '{args.strategy}'.")
    print(f"Final recall accuracy: {recall_accuracy[-1]:.2f}")

    if args.report:
        generate_report(recall_accuracy, args.tasks, args.strategy)

if __name__ == "__main__":
    main()