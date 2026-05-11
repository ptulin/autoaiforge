import psutil
import matplotlib.pyplot as plt
import time
import functools
from typing import Callable

def profile_memory(func: Callable):
    """
    A decorator to profile memory usage during the execution of a function.
    Logs memory usage over time and optionally generates a memory usage graph.
    
    Args:
        func (Callable): The function to be profiled.
    
    Returns:
        Callable: The wrapped function with memory profiling.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        memory_usage = []
        timestamps = []

        def monitor():
            """Monitor memory usage and record it."""
            process = psutil.Process()
            while not stop_monitoring:
                memory_usage.append(process.memory_info().rss / (1024 * 1024))  # Convert to MB
                timestamps.append(time.time() - start_time)
                time.sleep(0.1)  # Sample memory every 100ms

        # Start monitoring in a separate thread
        import threading
        stop_monitoring = False
        start_time = time.time()
        monitor_thread = threading.Thread(target=monitor)
        monitor_thread.start()

        try:
            result = func(*args, **kwargs)
        finally:
            stop_monitoring = True
            monitor_thread.join()

        # Log memory usage
        print(f"Memory usage during '{func.__name__}':")
        for t, mem in zip(timestamps, memory_usage):
            print(f"Time: {t:.2f}s, Memory: {mem:.2f} MB")

        # Generate memory usage graph
        plt.figure(figsize=(10, 6))
        plt.plot(timestamps, memory_usage, label='Memory Usage (MB)')
        plt.xlabel('Time (s)')
        plt.ylabel('Memory Usage (MB)')
        plt.title(f'Memory Usage Profile for {func.__name__}')
        plt.legend()
        plt.grid()
        plt.savefig(f"{func.__name__}_memory_profile.png")
        plt.close()

        return result

    return wrapper

if __name__ == "__main__":
    import argparse

    def example_function():
        """Example function to demonstrate memory profiling."""
        data = []
        for i in range(1000000):
            data.append(i)
        return sum(data)

    parser = argparse.ArgumentParser(description="Memory Usage Profiler")
    parser.add_argument('--example', action='store_true', help="Run the example function with memory profiling.")
    args = parser.parse_args()

    if args.example:
        profiled_example = profile_memory(example_function)
        profiled_example()