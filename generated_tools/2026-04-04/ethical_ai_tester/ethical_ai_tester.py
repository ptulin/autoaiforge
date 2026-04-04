import argparse
import json
import pandas as pd
import numpy as np
import yaml
from typing import Callable, Dict, Any

class EthicalAITester:
    """
    A framework to test AI systems for ethical compliance.
    """

    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.results = []

    def test_bias(self, model: Callable, test_data: pd.DataFrame):
        """
        Test for bias in the AI system.
        """
        if test_data.empty:
            self.results.append({"test": "bias", "result": "failed", "reason": "Empty test data"})
            return

        group_column = self.config['bias'].get('group_column')
        input_column = self.config['bias'].get('input_column')
        threshold = self.config['bias'].get('threshold', 0.1)

        if group_column not in test_data.columns or input_column not in test_data.columns:
            self.results.append({"test": "bias", "result": "failed", "reason": "Missing required columns in test data"})
            return

        groups = test_data[group_column].unique()
        outputs = {}
        for group in groups:
            group_data = test_data[test_data[group_column] == group]
            outputs[group] = model(group_data[input_column].tolist())

        # Calculate mean output per group
        means = {group: np.mean(outputs[group]) for group in outputs}
        max_diff = max(means.values()) - min(means.values())

        if max_diff > threshold:
            self.results.append({"test": "bias", "result": "failed", "reason": f"Bias detected with max difference {max_diff}"})
        else:
            self.results.append({"test": "bias", "result": "passed"})

    def test_fairness(self, model: Callable, test_data: pd.DataFrame):
        """
        Test for fairness in the AI system.
        """
        if test_data.empty:
            self.results.append({"test": "fairness", "result": "failed", "reason": "Empty test data"})
            return

        input_column = self.config['fairness'].get('input_column')
        min_unique_predictions = self.config['fairness'].get('min_unique_predictions', 2)

        if input_column not in test_data.columns:
            self.results.append({"test": "fairness", "result": "failed", "reason": "Missing required input column in test data"})
            return

        predictions = model(test_data[input_column].tolist())
        unique_predictions = len(set(predictions))

        if unique_predictions < min_unique_predictions:
            self.results.append({"test": "fairness", "result": "failed", "reason": "Insufficient unique predictions"})
        else:
            self.results.append({"test": "fairness", "result": "passed"})

    def run_tests(self, model: Callable, test_data: pd.DataFrame):
        """
        Run all configured tests.
        """
        if 'bias' in self.config:
            self.test_bias(model, test_data)
        if 'fairness' in self.config:
            self.test_fairness(model, test_data)

    def generate_report(self, output_format: str = 'console') -> Any:
        """
        Generate a compliance report.
        """
        if output_format == 'console':
            for result in self.results:
                print(result)
        elif output_format == 'json':
            return json.dumps(self.results, indent=4)
        elif output_format == 'csv':
            df = pd.DataFrame(self.results)
            return df.to_csv(index=False)
        else:
            raise ValueError("Unsupported output format")


def main():
    parser = argparse.ArgumentParser(description="Ethical AI Tester")
    parser.add_argument('--config', type=str, required=True, help="Path to YAML configuration file")
    parser.add_argument('--data', type=str, required=True, help="Path to CSV test data file")
    parser.add_argument('--output', type=str, default='console', choices=['console', 'json', 'csv'], help="Output format")
    args = parser.parse_args()

    # Load configuration
    try:
        with open(args.config, 'r') as f:
            config = yaml.safe_load(f)
    except Exception as e:
        print(f"Error loading configuration file: {e}")
        return

    # Load test data
    try:
        test_data = pd.read_csv(args.data)
    except Exception as e:
        print(f"Error loading test data file: {e}")
        return

    # Define a dummy model for testing purposes
    def dummy_model(inputs):
        return [x * 0.1 for x in inputs]

    tester = EthicalAITester(config)
    tester.run_tests(dummy_model, test_data)

    report = tester.generate_report(args.output)
    if args.output == 'json':
        print(report)
    elif args.output == 'csv':
        with open('report.csv', 'w') as f:
            f.write(report)

if __name__ == "__main__":
    main()