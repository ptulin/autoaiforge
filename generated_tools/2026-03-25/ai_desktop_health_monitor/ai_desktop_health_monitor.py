import psutil
import argparse
import json
import time
from unittest.mock import Mock

def monitor_system(cpu_threshold, claude_action_file, poll_interval):
    """
    Monitor the system for high CPU usage and take action using Claude AI.

    Args:
        cpu_threshold (int): CPU usage percentage threshold to trigger action.
        claude_action_file (str): Path to JSON file with Claude AI instructions.
        poll_interval (int): Interval in seconds to check system performance.
    """
    try:
        with open(claude_action_file, 'r') as f:
            claude_instructions = json.load(f)
    except FileNotFoundError:
        print(f"Error: Action file '{claude_action_file}' not found.")
        return
    except json.JSONDecodeError:
        print(f"Error: Action file '{claude_action_file}' is not a valid JSON file.")
        return

    anthropic_client = Mock()  # Replace actual API client with a mock for testing

    try:
        while True:
            cpu_usage = psutil.cpu_percent(interval=1)
            print(f"Current CPU usage: {cpu_usage}%")

            if cpu_usage > cpu_threshold:
                print(f"CPU usage exceeded threshold ({cpu_threshold}%). Taking action...")
                response = anthropic_client.completions.create(
                    model="claude-v1",
                    prompt=f"{claude_instructions['prompt']}\nCPU usage is {cpu_usage}%.",
                    max_tokens_to_sample=100
                )
                action = response.get("completion", "No action suggested.")
                print(f"Claude AI suggested action: {action}")

            time.sleep(poll_interval)

    except KeyboardInterrupt:
        print("Monitoring stopped by user.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="AI Desktop Health Monitor")
    parser.add_argument("--cpu-threshold", type=int, required=True, help="CPU usage percentage threshold to trigger actions.")
    parser.add_argument("--claude-action-file", type=str, required=True, help="Path to JSON file with Claude AI instructions.")
    parser.add_argument("--poll-interval", type=int, default=5, help="Polling interval in seconds (default: 5).")

    args = parser.parse_args()

    monitor_system(args.cpu_threshold, args.claude_action_file, args.poll_interval)
