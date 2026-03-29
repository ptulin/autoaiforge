# Claude Slack Workflow Bot

## Description

The Claude Slack Workflow Bot is a CLI tool designed to automate the creation of Slack workflows integrated with Claude AI. It allows developers to set up triggers (such as messages or events) that invoke Claude to process and respond intelligently. This is particularly useful for team collaboration and prompt-based task automation.

## Features

- Automates the creation of Slack workflows.
- Monitors specific Slack channels for triggers.
- Integrates with Claude AI for intelligent responses.

## Requirements

- Python 3.7+
- `slack_sdk`
- `pytest` (for testing)

## Installation

1. Clone this repository:
   ```bash
   git clone <repository_url>
   cd <repository_folder>
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

Run the CLI tool with the following arguments:

```bash
python claude_slack_workflow_bot.py --slack-token <your-slack-token> --trigger <#channel-name> --prompt <prompt-logic>
```

### Arguments

- `--slack-token`: Your Slack API token.
- `--trigger`: The Slack channel to monitor (e.g., `#general`).
- `--prompt`: The prompt logic for Claude AI.

### Example

```bash
python claude_slack_workflow_bot.py --slack-token xoxb-1234567890-abcdef --trigger #general --prompt "Summarize this conversation."
```

## Running Tests

To run the tests, use `pytest`:

```bash
pytest test_claude_slack_workflow_bot.py
```

## Notes

- This tool simulates the creation of a Slack workflow since Slack does not provide a direct API for workflow creation.
- Ensure you have the correct Slack API token and channel name before running the tool.

## License

This project is licensed under the MIT License.