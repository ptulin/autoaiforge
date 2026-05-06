import argparse
import yaml
import requests
from tenacity import retry, stop_after_attempt, wait_fixed

class WorkflowOrchestrator:
    def __init__(self, workflow_config):
        self.workflow = workflow_config

    @retry(stop=stop_after_attempt(3), wait=wait_fixed(2))
    def call_api(self, step):
        """Call an external API with retries."""
        response = requests.post(step['url'], json=step.get('payload', {}), headers=step.get('headers', {}))
        response.raise_for_status()
        return response.json()

    def execute_step(self, step):
        """Execute a single step in the workflow."""
        if step['type'] == 'api_call':
            return self.call_api(step)
        elif step['type'] == 'python_function':
            func = step['function']
            return func(*step.get('args', []), **step.get('kwargs', {}))
        else:
            raise ValueError(f"Unsupported step type: {step['type']}")

    def run(self):
        """Run the entire workflow."""
        results = {}
        for step_name, step in self.workflow.items():
            try:
                results[step_name] = self.execute_step(step)
            except Exception as e:
                results[step_name] = {'error': str(e)}
        return results

def load_workflow(file_path):
    """Load a workflow configuration from a YAML file."""
    with open(file_path, 'r') as file:
        return yaml.safe_load(file)

def main():
    parser = argparse.ArgumentParser(description="AI Workflow Orchestrator")
    parser.add_argument('--workflow', required=True, help="Path to the workflow YAML file")
    args = parser.parse_args()

    try:
        workflow_config = load_workflow(args.workflow)
        orchestrator = WorkflowOrchestrator(workflow_config)
        results = orchestrator.run()
        print("Workflow execution results:")
        print(yaml.dump(results, default_flow_style=False))
    except FileNotFoundError:
        print(f"Error: Workflow file '{args.workflow}' not found.")
    except yaml.YAMLError as e:
        print(f"Error: Failed to parse YAML file. {e}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()