import psutil
import matplotlib.pyplot as plt
import time
import threading
from functools import wraps

def monitor(model_function, *args, **kwargs):
    """
    Monitors resource utilization (CPU, memory) and logs performance metrics
    while running the provided model function.

    Parameters:
        model_function (callable): The function representing the LLM execution.
        *args: Positional arguments to pass to the model function.
        **kwargs: Keyword arguments to pass to the model function.

    Returns:
        The result of the model function execution.
    """
    resource_data = {
        'time': [],
        'cpu': [],
        'memory': []
    }

    def collect_metrics():
        while monitoring["running"]:
            resource_data['time'].append(time.time() - start_time)
            resource_data['cpu'].append(psutil.cpu_percent(interval=None))
            resource_data['memory'].append(psutil.virtual_memory().percent)
            time.sleep(0.5)

    def plot_metrics():
        plt.figure(figsize=(10, 6))
        plt.plot(resource_data['time'], resource_data['cpu'], label='CPU Usage (%)')
        plt.plot(resource_data['time'], resource_data['memory'], label='Memory Usage (%)')
        plt.xlabel('Time (s)')
        plt.ylabel('Usage (%)')
        plt.title('Resource Utilization Over Time')
        plt.legend()
        plt.grid()
        plt.show()

    monitoring = {"running": True}
    start_time = time.time()

    # Start the monitoring thread
    monitor_thread = threading.Thread(target=collect_metrics)
    monitor_thread.start()

    try:
        # Run the model function
        result = model_function(*args, **kwargs)
    finally:
        # Stop monitoring and wait for the thread to finish
        monitoring["running"] = False
        monitor_thread.join()

        # Plot the metrics
        plot_metrics()

    return result

if __name__ == "__main__":
    def dummy_model(duration):
        """A dummy model function to simulate workload."""
        start = time.time()
        while time.time() - start < duration:
            sum(i * i for i in range(10000))

    print("Starting LLM Runtime Monitor with a dummy model...")
    monitor(dummy_model, 5)