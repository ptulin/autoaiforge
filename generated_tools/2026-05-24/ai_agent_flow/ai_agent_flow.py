import yaml
import logging
import click
from openai import ChatCompletion

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def load_workflow_config(config_path):
    """Load the YAML configuration file."""
    try:
        with open(config_path, 'r') as file:
            return yaml.safe_load(file)
    except FileNotFoundError:
        logger.error("Configuration file not found.")
        raise
    except yaml.YAMLError as e:
        logger.error("Error parsing YAML file: %s", e)
        raise

def execute_agent(agent_config, input_data):
    """Execute a single AI agent based on the configuration."""
    try:
        if agent_config['type'] == 'openai':
            response = ChatCompletion.create(
                model=agent_config['model'],
                messages=[{"role": "user", "content": input_data}]
            )
            return response['choices'][0]['message']['content']
        else:
            raise ValueError(f"Unsupported agent type: {agent_config['type']}")
    except Exception as e:
        logger.error("Error executing agent: %s", e)
        raise

def execute_workflow(config):
    """Execute the workflow as defined in the configuration."""
    results = {}
    for step in config['workflow']:
        agent_name = step['agent']
        input_data = step.get('input', '')

        # Replace placeholders with previous results
        if isinstance(input_data, str):
            try:
                input_data = input_data.format(**results)
            except KeyError as e:
                logger.error("Missing placeholder value for: %s", e)
                raise

        logger.info("Executing step: %s", step['name'])
        agent_config = config['agents'][agent_name]
        result = execute_agent(agent_config, input_data)
        results[step['name']] = result

    return results

@click.command()
@click.option('--config', required=True, type=click.Path(exists=True), help='Path to the workflow configuration file.')
@click.option('--output', type=click.Path(), help='Path to save the workflow results.')
def main(config, output):
    """Main entry point for the AI Agent Workflow Orchestrator."""
    try:
        workflow_config = load_workflow_config(config)
        results = execute_workflow(workflow_config)

        logger.info("Workflow completed successfully.")
        for step, result in results.items():
            logger.info("Step: %s, Result: %s", step, result)

        if output:
            with open(output, 'w') as file:
                yaml.safe_dump(results, file)
            logger.info("Results saved to %s", output)

    except Exception as e:
        logger.error("Workflow execution failed: %s", e)
        raise

if __name__ == "__main__":
    main()