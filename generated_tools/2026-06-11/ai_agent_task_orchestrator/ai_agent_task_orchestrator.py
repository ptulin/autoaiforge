import argparse
import json
import yaml
import os
from openai import ChatCompletion

class AIAgentTaskOrchestrator:
    def __init__(self, config_path, input_path, output_path):
        self.config_path = config_path
        self.input_path = input_path
        self.output_path = output_path
        self.workflow = None

    def load_config(self):
        try:
            with open(self.config_path, 'r') as file:
                if self.config_path.endswith('.yaml') or self.config_path.endswith('.yml'):
                    self.workflow = yaml.safe_load(file)
                elif self.config_path.endswith('.json'):
                    self.workflow = json.load(file)
                else:
                    raise ValueError("Unsupported configuration file format. Use YAML or JSON.")

            if not self.workflow or 'steps' not in self.workflow or not isinstance(self.workflow['steps'], list):
                raise ValueError("Invalid workflow configuration format.")

        except (yaml.YAMLError, json.JSONDecodeError, ValueError) as e:
            raise RuntimeError(f"Failed to load configuration: {e}")

    def execute_workflow(self):
        if not self.workflow or 'steps' not in self.workflow or not self.workflow['steps']:
            raise RuntimeError("Workflow configuration is not loaded or is invalid.")

        results = {}
        for step in self.workflow.get('steps', []):
            step_name = step.get('name', 'Unnamed Step')
            model = step.get('model', 'gpt-3.5-turbo')
            prompt = step.get('prompt', '')

            if not prompt:
                raise ValueError(f"Step '{step_name}' is missing a prompt.")

            try:
                response = self.run_ai_model(model, prompt)
                results[step_name] = response
            except Exception as e:
                results[step_name] = f"Error: {e}"

        self.save_results(results)

    def run_ai_model(self, model, prompt):
        try:
            response = ChatCompletion.create(
                model=model,
                messages=[{"role": "user", "content": prompt}]
            )
            return response['choices'][0]['message']['content']
        except Exception as e:
            raise RuntimeError(f"Failed to execute AI model '{model}': {e}")

    def save_results(self, results):
        try:
            os.makedirs(self.output_path, exist_ok=True)
            output_file = os.path.join(self.output_path, 'results.json')
            with open(output_file, 'w') as file:
                json.dump(results, file, indent=4)
        except Exception as e:
            raise RuntimeError(f"Failed to save results: {e}")


def main():
    parser = argparse.ArgumentParser(description="AI Agent Task Orchestrator")
    parser.add_argument('--config', required=True, help="Path to the workflow configuration file (YAML/JSON).")
    parser.add_argument('--input', required=False, help="Path to the input file for the AI agents.")
    parser.add_argument('--output', required=True, help="Directory to save the results.")

    args = parser.parse_args()

    orchestrator = AIAgentTaskOrchestrator(
        config_path=args.config,
        input_path=args.input,
        output_path=args.output
    )

    try:
        orchestrator.load_config()
        orchestrator.execute_workflow()
        print(f"Workflow executed successfully. Results saved to {args.output}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
