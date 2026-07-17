# Agent Manager

Agent Manager is a CLI tool that enables developers to deploy, manage, and monitor self-hosted AI agents locally. This tool provides features to start/stop agents, view resource usage, and handle agent configurations, making it easier to experiment with and maintain AI agents without relying on cloud services.

## Features

- Start an AI agent using a configuration file.
- Stop a running AI agent by its PID.
- Monitor the resource usage (CPU and memory) of a running AI agent.
- Validate the configuration file for correctness.

## Installation

1. Clone the repository:
   ```bash
   git clone <repository_url>
   cd agent_manager
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

Run the tool using the command line:

### Start an AI Agent
```bash
python agent_manager.py start <config_path>
```

### Stop an AI Agent
```bash
python agent_manager.py stop <pid>
```

### Monitor Resource Usage
```bash
python agent_manager.py monitor <pid>
```

### Validate Configuration File
```bash
python agent_manager.py validate <config_path>
```

## Configuration File Format

The configuration file should be in YAML format and must include a `command` field. Example:

```yaml
command: python my_agent.py --arg1 value1 --arg2 value2
```

## Testing

Run the tests using `pytest`:

```bash
pytest test_agent_manager.py
```

## Requirements

- Python 3.7+
- `psutil`
- `pyyaml`

Install dependencies using:
```bash
pip install -r requirements.txt
```

## License

This project is licensed under the MIT License.