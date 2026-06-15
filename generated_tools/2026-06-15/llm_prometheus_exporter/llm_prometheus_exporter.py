import argparse
import time
from prometheus_client import start_http_server, Gauge
import psutil
import requests

# Define Prometheus metrics
latency_gauge = Gauge('llm_inference_latency_seconds', 'Latency of LLM inference in seconds')
token_usage_gauge = Gauge('llm_token_usage', 'Number of tokens used in LLM inference')
memory_usage_gauge = Gauge('llm_memory_usage_bytes', 'Memory usage of the LLM process in bytes')
error_count_gauge = Gauge('llm_error_count', 'Number of errors during LLM inference')

def fetch_llm_metrics(endpoint):
    """Fetch metrics from the LLM endpoint."""
    try:
        start_time = time.time()
        response = requests.get(endpoint, timeout=5)
        response.raise_for_status()
        latency = time.time() - start_time
        data = response.json()

        latency_gauge.set(latency)
        token_usage_gauge.set(data.get('token_usage', 0))
        memory_usage_gauge.set(data.get('memory_usage', 0))
        error_count_gauge.set(data.get('error_count', 0))
    except requests.RequestException as e:
        error_count_gauge.inc()
        print(f"Error fetching metrics from LLM endpoint: {e}")

def monitor_metrics(llm_endpoint, refresh_interval):
    """Continuously fetch and update metrics."""
    while True:
        fetch_llm_metrics(llm_endpoint)
        time.sleep(refresh_interval)

def main():
    parser = argparse.ArgumentParser(description="LLM Prometheus Exporter")
    parser.add_argument('--llm-endpoint', required=True, help="URL of the LLM endpoint to monitor")
    parser.add_argument('--port', type=int, default=9090, help="Port to expose Prometheus metrics (default: 9090)")
    parser.add_argument('--refresh-interval', type=int, default=10, help="Metrics refresh interval in seconds (default: 10)")
    args = parser.parse_args()

    # Start the Prometheus metrics server
    start_http_server(args.port)
    print(f"Prometheus metrics server started on port {args.port}")

    # Start monitoring the LLM metrics
    monitor_metrics(args.llm_endpoint, args.refresh_interval)

if __name__ == "__main__":
    main()