import argparse
import numpy as np
import matplotlib.pyplot as plt

def exponential_decay(rate, duration):
    """Simulate exponential memory decay."""
    time = np.arange(0, duration + 1)
    memory = np.exp(-rate * time)
    return time, memory

def linear_decay(rate, duration):
    """Simulate linear memory decay."""
    time = np.arange(0, duration + 1)
    memory = np.maximum(1 - rate * time, 0)
    return time, memory

def simulate_decay(strategy, rate, duration):
    """Simulate memory decay based on the given strategy."""
    if strategy == "exponential":
        return exponential_decay(rate, duration)
    elif strategy == "linear":
        return linear_decay(rate, duration)
    else:
        raise ValueError("Unsupported strategy. Choose 'exponential' or 'linear'.")

def plot_decay(time, memory, strategy, rate, duration):
    """Plot memory decay over time."""
    plt.figure(figsize=(8, 5))
    plt.plot(time, memory, label=f"{strategy.capitalize()} Decay (rate={rate})")
    plt.title("Memory Decay Simulation")
    plt.xlabel("Time")
    plt.ylabel("Memory Retention")
    plt.ylim(0, 1.1)
    plt.grid(True)
    plt.legend()
    plt.savefig("memory_decay_simulation.png")
    plt.show()

def main():
    parser = argparse.ArgumentParser(
        description="Memory Decay Simulation Tool"
    )
    parser.add_argument(
        "--strategy", 
        type=str, 
        choices=["exponential", "linear"], 
        required=True, 
        help="Decay strategy: 'exponential' or 'linear'"
    )
    parser.add_argument(
        "--rate", 
        type=float, 
        required=True, 
        help="Decay rate (positive float)"
    )
    parser.add_argument(
        "--duration", 
        type=int, 
        required=True, 
        help="Duration of the simulation (positive integer)"
    )

    args = parser.parse_args()

    if args.rate <= 0 or args.duration <= 0:
        print("Error: Rate and duration must be positive values.")
        return

    try:
        time, memory = simulate_decay(args.strategy, args.rate, args.duration)
        plot_decay(time, memory, args.strategy, args.rate, args.duration)
    except ValueError as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()