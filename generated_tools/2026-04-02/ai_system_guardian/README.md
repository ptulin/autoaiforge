# AI System Guardian

AI System Guardian provides a secure wrapper for monitoring and logging actions performed by AI agents during system automation tasks. It ensures transparency by capturing agent commands, their execution outcomes, and potential anomalies, making it vital for debugging and compliance in AI-driven automation.

## Features
- Monitors and logs AI agent actions.
- Executes only pre-approved commands.
- Reloads configuration dynamically when the file is updated.
- Provides detailed logging for debugging and compliance.

## Installation

Install the required dependencies using pip:

```bash
pip install watchdog
```

## Usage

Run the tool with the path to the configuration file:

```bash
python ai_system_guardian.py --config /path/to/config.json
```

## Configuration File Format

The configuration file should be a JSON file with the following structure:

```json
{
  "allowed_commands": ["echo Hello"],
  "tasks": [
    {"command": "echo Hello"}
  ],
  "log_file": "ai_system_guardian.log"
}
```

- `allowed_commands`: A list of commands that are allowed to be executed.
- `tasks`: A list of tasks, each containing a `command` to execute.
- `log_file`: The path to the log file where actions will be logged.

## Testing

Run the tests using pytest:

```bash
pytest test_ai_system_guardian.py
```

The tests include:
- Loading configuration files.
- Executing allowed and blocked commands.
- Handling tasks from the configuration.

## License

This project is licensed under the MIT License.