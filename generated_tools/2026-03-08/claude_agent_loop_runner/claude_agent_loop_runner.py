import argparse
import json
import yaml
from anthropic import Anthropic
from rich.console import Console
from rich.logging import RichHandler
import logging

# Set up logging
console = Console()
logging.basicConfig(level=logging.INFO, handlers=[RichHandler(console=console)])
logger = logging.getLogger("ClaudeAgentLoopRunner")

def load_workflow(file_path):
    """Load workflow from a JSON or YAML file."""
    try:
        with open(file_path, 'r') as file:
            content = file.read()
            if file_path.endswith('.json'):
                return json.loads(content)
            elif file_path.endswith('.yaml') or file_path.endswith('.yml'):
                return yaml.safe_load(content)
            else:
                raise ValueError("Unsupported file format. Use JSON or YAML.")
    except Exception as e:
        logger.error(f"Failed to load workflow: {e}")
        raise

def execute_workflow(workflow, anthropic_client, max_iterations):
    """Execute the workflow using the Claude AI SDK."""
    try:
        for step in workflow.get("steps", []):
            if max_iterations <= 0:
                logger.info("Max iterations reached. Exiting.")
                break

            prompt = step.get("prompt")
            if not prompt:
                logger.warning("Step missing 'prompt'. Skipping.")
                continue

            logger.info(f"Executing step: {step.get('name', 'Unnamed Step')}")
            response = anthropic_client.completions.create(
                model="claude-v1",
                prompt=prompt,
                max_tokens_to_sample=step.get("max_tokens", 100)
            )

            logger.info(f"Response: {response.get('completion', 'No response')}") if response else logger.info("No response received.")
            max_iterations -= 1
    except Exception as e:
        logger.error(f"Error during workflow execution: {e}")
        raise

def main():
    """Main function for CLI."""
    parser = argparse.ArgumentParser(description="Claude Agent Loop Runner")
    parser.add_argument("--workflow", required=True, help="Path to the workflow file (JSON/YAML).")
    parser.add_argument("--max-iterations", type=int, default=10, help="Maximum number of iterations.")
    parser.add_argument("--api-key", required=True, help="Anthropic API key.")

    args = parser.parse_args()

    try:
        workflow = load_workflow(args.workflow)
        anthropic_client = Anthropic(api_key=args.api_key)
        execute_workflow(workflow, anthropic_client, args.max_iterations)
    except Exception as e:
        logger.error(f"Failed to run Claude Agent Loop Runner: {e}")

if __name__ == "__main__":
    main()
