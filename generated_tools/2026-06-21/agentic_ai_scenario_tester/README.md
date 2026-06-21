# Agentic AI Scenario Tester

## Overview
The Agentic AI Scenario Tester is a CLI tool that allows developers to simulate complex scenarios and test how agentic AI systems respond to various conditions. It evaluates decision-making reliability, adaptability, and performance across diverse environments.

## Features
- Validate scenario JSON files against a predefined schema.
- Simulate scenarios with multiple goals and constraints.
- Generate detailed reports in CSV and JSON formats.
- Create performance graphs for each scenario.

## Installation
To use this tool, install the required dependencies:

```bash
pip install pandas matplotlib jsonschema
```

## Usage
Run the tool from the command line:

```bash
python agentic_ai_scenario_tester.py --scenario <path_to_scenario_file> --output <output_directory>
```

### Arguments
- `--scenario`: Path to the scenario JSON file.
- `--output`: Directory to save the results (logs, reports, and graphs).

## Example
Given a scenario file `example_scenario.json`:

```json
{
  "scenarios": [
    {
      "name": "ExampleScenario",
      "goals": ["goal1", "goal2"],
      "constraints": ["constraint1"],
      "environment": {}
    }
  ]
}
```

Run the tool as follows:

```bash
python agentic_ai_scenario_tester.py --scenario example_scenario.json --output results
```

This will generate the following files in the `results` directory:
- `ExampleScenario_log.csv`: A CSV file containing the simulation log.
- `ExampleScenario_report.json`: A JSON file containing the simulation results.
- `ExampleScenario_performance.png`: A graph showing the performance of the scenario.

## Testing
To run the tests, install `pytest`:

```bash
pip install pytest
```

Run the tests using:

```bash
pytest test_agentic_ai_scenario_tester.py
```

The tests include:
- Validating a correctly formatted scenario file.
- Handling invalid JSON schema.
- Generating reports and verifying file operations.
- Handling missing scenario files gracefully.

## License
This project is licensed under the MIT License.