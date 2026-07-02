# Sandbox Action Visualizer

## Description

This CLI tool takes action logs from AI sandbox environments and generates interactive visualizations of agent behaviors over time. By plotting actions on a timeline or within a spatial sandbox context, it allows developers to better understand agent decisions and anomalies for auditing and debugging.

## Installation

Install the required Python packages:

```bash
pip install pandas matplotlib
```

## Usage

Run the tool with the following command:

```bash
python sandbox_action_visualizer.py --logfile <path_to_log_file> [--output <output_image_path>] [--filter-agent <agent_id>] [--filter-action <action_type>]
```

### Arguments

- `--logfile`: Path to the AI agent log file (JSON or CSV).
- `--output`: Path to save the visualization image (optional).
- `--filter-agent`: Filter logs by a specific agent ID (optional).
- `--filter-action`: Filter logs by a specific action type (optional).

### Example

```bash
python sandbox_action_visualizer.py --logfile logs.json --output visualization.png --filter-agent agent_1
```

## Testing

To run the tests:

```bash
pytest test_sandbox_action_visualizer.py
```

## License

MIT License