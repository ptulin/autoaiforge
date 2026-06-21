import argparse
import json
import os
import pandas as pd
import matplotlib.pyplot as plt
from jsonschema import validate, ValidationError

SCHEMA = {
    "type": "object",
    "properties": {
        "scenarios": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "name": {"type": "string"},
                    "goals": {"type": "array", "items": {"type": "string"}},
                    "constraints": {"type": "array", "items": {"type": "string"}},
                    "environment": {"type": "object"}
                },
                "required": ["name", "goals", "constraints", "environment"]
            }
        }
    },
    "required": ["scenarios"]
}

def load_scenario(file_path):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Scenario file '{file_path}' does not exist.")

    with open(file_path, 'r') as f:
        try:
            data = json.load(f)
            validate(instance=data, schema=SCHEMA)
            return data
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON format: {e}")
        except ValidationError as e:
            raise ValueError(f"JSON schema validation error: {e}")

def simulate_scenario(scenario):
    results = []
    for step, goal in enumerate(scenario['goals'], start=1):
        result = {
            'step': step,
            'goal': goal,
            'decision': f"Decision for {goal}",
            'outcome': "Success" if step % 2 == 0 else "Failure"
        }
        results.append(result)
    return results

def generate_report(scenarios, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    for scenario in scenarios:
        results = simulate_scenario(scenario)
        df = pd.DataFrame(results)

        # Save log file
        log_file = os.path.join(output_dir, f"{scenario['name']}_log.csv")
        df.to_csv(log_file, index=False)

        # Save JSON report
        report_file = os.path.join(output_dir, f"{scenario['name']}_report.json")
        with open(report_file, 'w') as f:
            json.dump(results, f, indent=4)

        # Generate graph
        plt.figure()
        df['outcome_numeric'] = df['outcome'].apply(lambda x: 1 if x == "Success" else 0)
        plt.plot(df['step'], df['outcome_numeric'], marker='o', label='Outcome')
        plt.title(f"Scenario: {scenario['name']}")
        plt.xlabel("Step")
        plt.ylabel("Outcome (1=Success, 0=Failure)")
        plt.legend()
        graph_file = os.path.join(output_dir, f"{scenario['name']}_performance.png")
        plt.savefig(graph_file)
        plt.close()

def main():
    parser = argparse.ArgumentParser(description="Agentic AI Scenario Tester")
    parser.add_argument('--scenario', required=True, help="Path to the scenario JSON file")
    parser.add_argument('--output', required=True, help="Directory to save the results")

    args = parser.parse_args()

    try:
        scenario_data = load_scenario(args.scenario)
        generate_report(scenario_data['scenarios'], args.output)
        print(f"Reports and logs have been saved to '{args.output}'")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()