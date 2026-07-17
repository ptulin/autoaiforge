import argparse
import os
import signal
import subprocess
import psutil
import yaml
from typing import Optional

def start_agent(config_path: str):
    """Start an AI agent using the provided configuration file."""
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"Configuration file '{config_path}' not found.")

    with open(config_path, 'r') as file:
        config = yaml.safe_load(file)

    if 'command' not in config:
        raise ValueError("Configuration file must contain a 'command' field.")

    command = config['command']
    process = subprocess.Popen(command, shell=True, preexec_fn=os.setsid)
    print(f"Agent started with PID {process.pid}.")
    return process.pid

def stop_agent(pid: int):
    """Stop a running AI agent by its PID."""
    try:
        os.killpg(os.getpgid(pid), signal.SIGTERM)
        print(f"Agent with PID {pid} has been stopped.")
    except ProcessLookupError:
        print(f"No process found with PID {pid}.")
    except OSError as e:
        print(f"Error stopping process with PID {pid}: {e}")

def monitor_resources(pid: int):
    """Monitor the resource usage of a running AI agent."""
    try:
        process = psutil.Process(pid)
        print(f"Monitoring resources for PID {pid}:")
        print(f"CPU Usage: {process.cpu_percent(interval=1.0)}%")
        print(f"Memory Usage: {process.memory_info().rss / (1024 * 1024):.2f} MB")
    except psutil.NoSuchProcess:
        print(f"No process found with PID {pid}.")

def validate_config(config_path: str):
    """Validate the configuration file."""
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"Configuration file '{config_path}' not found.")

    with open(config_path, 'r') as file:
        try:
            config = yaml.safe_load(file)
            if 'command' not in config:
                raise ValueError("Configuration file must contain a 'command' field.")
            print("Configuration file is valid.")
        except yaml.YAMLError as e:
            raise ValueError(f"Invalid YAML format: {e}")

def main():
    parser = argparse.ArgumentParser(description="Self-Hosted AI Agent Manager")
    subparsers = parser.add_subparsers(dest="command", required=True)

    start_parser = subparsers.add_parser("start", help="Start an AI agent")
    start_parser.add_argument("config", help="Path to the agent configuration file")

    stop_parser = subparsers.add_parser("stop", help="Stop a running AI agent")
    stop_parser.add_argument("pid", type=int, help="PID of the agent to stop")

    monitor_parser = subparsers.add_parser("monitor", help="Monitor resource usage of an AI agent")
    monitor_parser.add_argument("pid", type=int, help="PID of the agent to monitor")

    validate_parser = subparsers.add_parser("validate", help="Validate an agent configuration file")
    validate_parser.add_argument("config", help="Path to the agent configuration file")

    args = parser.parse_args()

    try:
        if args.command == "start":
            start_agent(args.config)
        elif args.command == "stop":
            stop_agent(args.pid)
        elif args.command == "monitor":
            monitor_resources(args.pid)
        elif args.command == "validate":
            validate_config(args.config)
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
