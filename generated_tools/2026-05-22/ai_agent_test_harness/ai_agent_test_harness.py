import argparse
import yaml
import requests
from rich.console import Console
from rich.table import Table
from datetime import datetime
import os

def load_test_config(file_path):
    """Load test configuration from a YAML file."""
    try:
        with open(file_path, 'r') as file:
            return yaml.safe_load(file)
    except FileNotFoundError:
        raise FileNotFoundError(f"Test configuration file not found: {file_path}")
    except yaml.YAMLError as e:
        raise ValueError(f"Error parsing YAML file: {e}")

def run_test_case(test_case, langsmith_api_key=None):
    """Run a single test case and compare the output with the expected result."""
    try:
        response = requests.post(
            test_case['endpoint'],
            json=test_case['input'],
            headers={"Authorization": f"Bearer {langsmith_api_key}"} if langsmith_api_key else {}
        )
        response.raise_for_status()
        actual_output = response.json()
        return actual_output == test_case['expected_output'], actual_output
    except requests.RequestException as e:
        return False, str(e)

def generate_summary_report(results, output_file):
    """Generate a summary report and save it to a log file."""
    console = Console()
    table = Table(title="Test Summary")
    table.add_column("Test Case", justify="left")
    table.add_column("Status", justify="center")
    table.add_column("Details", justify="left")

    with open(output_file, 'w') as log_file:
        timestamp = datetime.now().isoformat()
        log_file.write(f"Test Run - {timestamp}\n")
        log_file.write("=" * 50 + "\n")

        for test_name, result in results.items():
            status = "PASS" if result['status'] else "FAIL"
            table.add_row(test_name, status, str(result['details']))
            log_file.write(f"{test_name}: {status}\n")
            log_file.write(f"Details: {result['details']}\n\n")

        console.print(table)

def main():
    parser = argparse.ArgumentParser(description="AI Agent Test Harness")
    parser.add_argument('--test_config', type=str, required=True, help="Path to the YAML test configuration file.")
    parser.add_argument('--output', type=str, required=True, help="Path to the output log file.")
    parser.add_argument('--langsmith_api_key', type=str, help="Optional LangSmith API key for integration.")
    args = parser.parse_args()

    try:
        test_config = load_test_config(args.test_config)
    except (FileNotFoundError, ValueError) as e:
        print(f"Error: {e}")
        return

    results = {}
    for test_case in test_config.get('test_cases', []):
        test_name = test_case.get('name', 'Unnamed Test')
        status, details = run_test_case(test_case, args.langsmith_api_key)
        results[test_name] = {'status': status, 'details': details}

    generate_summary_report(results, args.output)

if __name__ == "__main__":
    main()
