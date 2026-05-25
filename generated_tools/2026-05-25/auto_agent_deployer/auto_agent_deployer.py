import argparse
import yaml
import boto3
import logging
import os

def setup_logging():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    return logging.getLogger('AutoAgentDeployer')

def parse_arguments():
    parser = argparse.ArgumentParser(description='Auto Agent Deployer: Deploy AI agents using YAML configuration.')
    parser.add_argument('--config', required=True, help='Path to the YAML configuration file.')
    return parser.parse_args()

def load_yaml_config(file_path):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Configuration file '{file_path}' not found.")
    with open(file_path, 'r') as file:
        return yaml.safe_load(file)

def deploy_to_aws_lambda(agent_config, logger):
    try:
        client = boto3.client('lambda')
        response = client.create_function(
            FunctionName=agent_config['name'],
            Runtime=agent_config['runtime'],
            Role=agent_config['role'],
            Handler=agent_config['handler'],
            Code={'ZipFile': agent_config['code_zip']},
            Description=agent_config.get('description', ''),
            Timeout=agent_config.get('timeout', 15),
            MemorySize=agent_config.get('memory_size', 128)
        )
        logger.info(f"Successfully deployed agent '{agent_config['name']}' to AWS Lambda.")
        return response
    except Exception as e:
        logger.error(f"Failed to deploy agent '{agent_config['name']}': {str(e)}")
        raise

def deploy_agents(config, logger):
    for agent in config.get('agents', []):
        if agent['type'] == 'aws_lambda':
            deploy_to_aws_lambda(agent, logger)
        else:
            logger.warning(f"Unsupported agent type '{agent['type']}' for agent '{agent['name']}'.")

def main():
    logger = setup_logging()
    args = parse_arguments()

    try:
        config = load_yaml_config(args.config)
        deploy_agents(config, logger)
    except Exception as e:
        logger.error(f"Error during deployment: {str(e)}")

if __name__ == '__main__':
    main()
