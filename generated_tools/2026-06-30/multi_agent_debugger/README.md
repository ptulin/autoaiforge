# Multi-Agent Debugger

## Description
The Multi-Agent Debugger is a command-line tool designed to help developers monitor, trace, and log interactions among multiple AI agents in real-time. It provides detailed insights into message passing, task execution times, and bottlenecks, enabling rapid troubleshooting of multi-agent systems.

## Features
- Real-time logging of inter-agent communication
- Task performance and execution time tracking
- Event filtering and customizable debugging levels
- Console-based visualizations using the `rich` library

## Installation

1. Clone the repository:
   ```bash
   git clone <repository_url>
   cd multi_agent_debugger
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

Run the tool with the following command:

```bash
python multi_agent_debugger.py --input <log_file.json> --level <info|verbose>
```

### Example

```bash
python multi_agent_debugger.py --input logs.json --level verbose
```

## Input Format
The input log file should be in JSON format and structured as an array of events. Each event should include the following keys:
- `timestamp`: The timestamp of the event
- `agent`: The name of the agent involved
- `event`: The type of event (e.g., `TaskStart`, `TaskEnd`)
- `details`: Additional details about the event

Example:

```json
[
    {"timestamp": "2023-10-01T12:00:00Z", "agent": "Agent1", "event": "TaskStart", "details": "Task A"},
    {"timestamp": "2023-10-01T12:01:00Z", "agent": "Agent2", "event": "TaskEnd", "details": "Task B"}
]
```

## Testing

Run tests using `pytest`:

```bash
pytest test_multi_agent_debugger.py
```

The test suite includes tests for:
- Parsing valid input files
- Handling missing files gracefully
- Handling invalid JSON input

## License
This project is licensed under the MIT License.