import argparse
import json
import logging
from typing import List, Dict
from langchain.llms import OpenAI
from langchain.chains import LLMChain

logging.basicConfig(level=logging.INFO)

def load_config(config_path: str) -> Dict:
    """Load the workflow configuration from a JSON file."""
    try:
        with open(config_path, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        logging.error(f"Configuration file not found: {config_path}")
        raise
    except json.JSONDecodeError:
        logging.error(f"Invalid JSON in configuration file: {config_path}")
        raise

def execute_workflow(config: Dict) -> Dict:
    """Execute the workflow based on the provided configuration."""
    results = {}

    for step in config.get("steps", []):
        step_name = step.get("name")
        model_name = step.get("model")
        task = step.get("task")
        api_key = step.get("api_key")

        if not all([step_name, model_name, task, api_key]):
            logging.error(f"Step {step_name or 'unknown'} is missing required fields.")
            results[step_name or 'unknown'] = None
            continue

        logging.info(f"Executing step: {step_name} with model: {model_name}")

        try:
            llm = OpenAI(model=model_name, openai_api_key=api_key)
            chain = LLMChain(llm=llm)
            result = chain.run(task)
            results[step_name] = result
        except Exception as e:
            logging.error(f"Error executing step {step_name}: {e}")
            results[step_name] = None

    return results

def main():
    parser = argparse.ArgumentParser(description="LLM Coordinator: Orchestrate workflows between multiple LLMs.")
    parser.add_argument('--config', required=True, help="Path to the JSON configuration file.")
    args = parser.parse_args()

    try:
        config = load_config(args.config)
        results = execute_workflow(config)
        print(json.dumps(results, indent=2))
    except Exception as e:
        logging.error(f"Failed to execute workflow: {e}")

if __name__ == "__main__":
    main()
