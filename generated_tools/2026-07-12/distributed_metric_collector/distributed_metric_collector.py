import psutil
import socket
import threading
import time
import matplotlib.pyplot as plt
from typing import List, Callable

class Collector:
    def __init__(self, nodes: List[str], metric_hooks: List[Callable] = None):
        """
        Initialize the Collector.

        :param nodes: List of node IPs to collect metrics from.
        :param metric_hooks: List of custom metric hooks (functions) to collect additional metrics.
        """
        self.nodes = nodes
        self.metric_hooks = metric_hooks if metric_hooks else []
        self.running = False
        self.data = {node: [] for node in nodes}
        self.lock = threading.Lock()

    def _collect_metrics(self, node: str):
        """Collect metrics from a single node."""
        while self.running:
            try:
                # Simulate metric collection (e.g., GPU usage, CPU usage)
                metrics = {
                    "cpu_usage": psutil.cpu_percent(interval=None),
                    "memory_usage": psutil.virtual_memory().percent,
                }

                # Apply custom metric hooks
                for hook in self.metric_hooks:
                    metrics.update(hook())

                with self.lock:
                    self.data[node].append(metrics)

                time.sleep(1)  # Ensure the thread doesn't run continuously

            except Exception as e:
                print(f"Error collecting metrics from {node}: {e}")

    def start(self):
        """Start collecting metrics from all nodes."""
        self.running = True
        self.threads = []
        for node in self.nodes:
            thread = threading.Thread(target=self._collect_metrics, args=(node,))
            thread.daemon = True  # Ensure threads exit when the main program exits
            thread.start()
            self.threads.append(thread)

    def stop(self):
        """Stop collecting metrics and join threads."""
        self.running = False
        for thread in self.threads:
            thread.join()

    def visualize(self, save_path: str = None):
        """
        Visualize the collected metrics.

        :param save_path: Optional path to save the plot as an image.
        """
        with self.lock:
            for node, metrics in self.data.items():
                if not metrics:
                    print(f"No metrics collected for node {node}.")
                    continue

                timestamps = range(len(metrics))
                cpu_usage = [m["cpu_usage"] for m in metrics]
                memory_usage = [m["memory_usage"] for m in metrics]

                plt.figure(figsize=(10, 5))
                plt.plot(timestamps, cpu_usage, label="CPU Usage (%)")
                plt.plot(timestamps, memory_usage, label="Memory Usage (%)")
                plt.title(f"Metrics for Node {node}")
                plt.xlabel("Time")
                plt.ylabel("Usage (%)")
                plt.legend()

                if save_path:
                    plt.savefig(f"{save_path}_{node}.png")
                else:
                    plt.show()

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Distributed Metric Collector")
    parser.add_argument("--nodes", nargs="+", required=True, help="List of node IPs")
    parser.add_argument("--save", help="Path to save the visualization")
    args = parser.parse_args()

    collector = Collector(nodes=args.nodes)
    collector.start()

    try:
        print("Collecting metrics. Press Ctrl+C to stop.")
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Stopping metric collection.")
        collector.stop()
        collector.visualize(save_path=args.save)
