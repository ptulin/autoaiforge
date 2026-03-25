# Workflow Trigger CLI

## Description
Workflow Trigger CLI is a Python-based command-line tool that enables developers to trigger and monitor automated workflows in Claude AI using predefined connectors. It supports asynchronous task execution, retry mechanisms, and real-time logging for robust automation.

## Features
- Trigger Claude AI workflows via CLI
- Pass custom input payloads in JSON format
- Support for asynchronous task execution
- Retry mechanism for handling failures
- Real-time logging and status updates

## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd workflow_trigger_cli
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

To trigger a workflow, use the following command:

```bash
python workflow_trigger_cli.py --workflow <workflow_name> --input <input_file_path> [--retries <num_retries>] [--delay <retry_delay_seconds>]
```

### Example

```bash
python workflow_trigger_cli.py --workflow my_workflow --input input.json --retries 3 --delay 5
```

- `--workflow`: Name of the workflow to trigger.
- `--input`: Path to a JSON file containing the input payload.
- `--retries`: (Optional) Number of retries on failure. Default is 3.
- `--delay`: (Optional) Delay between retries in seconds. Default is 5.

## Testing

To run the tests, use:

```bash
pytest test_workflow_trigger_cli.py
```

## Notes
- Ensure you have network access to the Claude AI API endpoint.
- Replace the `API_BASE_URL` in the code with the actual API endpoint for your workflows.

## License
This project is licensed under the MIT License.