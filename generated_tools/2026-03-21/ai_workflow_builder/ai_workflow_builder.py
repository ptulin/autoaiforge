import yaml
import click
import openai
import logging
from typing import Any, Dict, List

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def execute_ai_task(task: Dict[str, Any]) -> str:
    """Executes an AI task using OpenAI's API."""
    try:
        prompt = task.get('prompt', '')
        model = task.get('model', 'text-davinci-003')
        max_tokens = task.get('max_tokens', 100)

        logger.info(f"Executing AI task with model {model} and prompt: {prompt}")
        response = openai.Completion.create(
            engine=model,
            prompt=prompt,
            max_tokens=max_tokens
        )
        return response.choices[0].text.strip()
    except Exception as e:
        logger.error(f"Error executing AI task: {e}")
        raise

def execute_workflow(config: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Executes a workflow based on the provided configuration."""
    results = []
    for step in config.get('workflow', []):
        task_type = step.get('type')
        if task_type == 'ai_task':
            result = execute_ai_task(step)
            results.append({'step': step.get('name', 'Unnamed Step'), 'result': result})
        else:
            logger.warning(f"Unsupported task type: {task_type}")
            results.append({'step': step.get('name', 'Unnamed Step'), 'result': None, 'error': 'Unsupported task type'})
    return results

@click.command()
@click.option('--config', type=click.Path(exists=True), required=True, help='Path to the YAML configuration file.')
@click.option('--output', type=click.Path(writable=True), default=None, help='Optional path to save the workflow output.')
def main(config: str, output: str):
    """Main entry point for the AI Workflow Builder."""
    try:
        with open(config, 'r') as file:
            workflow_config = yaml.safe_load(file)

        logger.info("Loaded workflow configuration.")
        results = execute_workflow(workflow_config)

        if output:
            with open(output, 'w') as outfile:
                yaml.dump(results, outfile)
            logger.info(f"Workflow results saved to {output}")
        else:
            logger.info("Workflow results:")
            logger.info(results)

    except Exception as e:
        logger.error(f"Failed to execute workflow: {e}")

if __name__ == '__main__':
    main()
