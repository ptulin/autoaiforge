# Agent Health Monitor

This tool monitors the health and performance of deployed autonomous AI agents in real-time. It tracks key metrics such as response time, task success rates, and resource usage, alerting developers to potential issues before they escalate.

## Features
- Monitors CPU and memory usage of a specific process.
- Sends email alerts if CPU usage exceeds a threshold.
- Generates and saves a performance metrics chart.

## Installation

Install the required dependencies:

```bash
pip install psutil matplotlib typer
```

## Usage

Run the tool using the following command:

```bash
python agent_health_monitor.py --agent-id <PROCESS_ID> --alert-email <EMAIL> --duration <SECONDS>
```

### Arguments
- `--agent-id`: The process ID of the agent to monitor.
- `--alert-email`: (Optional) Email to send alerts to.
- `--duration`: (Optional) Duration in seconds to monitor the agent (default: 60).

## Testing

Run the tests using pytest:

```bash
pytest test_agent_health_monitor.py
```

## Notes
- Replace the SMTP server details in the `send_email_alert` function with your own credentials.
- Ensure the process ID you provide corresponds to a running process.
