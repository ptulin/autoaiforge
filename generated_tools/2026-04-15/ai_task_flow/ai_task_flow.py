import argparse
import json
import yaml
import logging
import networkx as nx
from openai import ChatCompletion

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def load_workflow(file_path):
    """Load workflow from a YAML or JSON file."""
    try:
        with open(file_path, 'r') as f:
            content = f.read()
            if file_path.endswith('.yaml') or file_path.endswith('.yml'):
                return yaml.safe_load(content)
            elif file_path.endswith('.json'):
                return json.loads(content)
            else:
                raise ValueError("Unsupported file format. Use YAML or JSON.")
    except Exception as e:
        logging.error(f"Error loading workflow file: {e}")
        raise

def execute_task(task, ai_model):
    """Execute a single task using AI model if specified."""
    try:
        if 'ai_step' in task:
            prompt = task['ai_step']['prompt']
            logging.info(f"Executing AI step for task: {task['name']}")
            response = ai_model.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}]
            )
            return response.choices[0].message['content']
        else:
            logging.info(f"Executing non-AI task: {task['name']}")
            return task.get('output', None)
    except Exception as e:
        logging.error(f"Error executing task {task['name']}: {e}")
        raise

def execute_workflow(workflow, ai_api_key):
    """Execute the workflow defined in the input file."""
    try:
        ai_model = ChatCompletion(api_key=ai_api_key)
        graph = nx.DiGraph()

        # Build the graph
        for task in workflow['tasks']:
            graph.add_node(task['name'], task=task)
            for dependency in task.get('dependencies', []):
                graph.add_edge(dependency, task['name'])

        # Execute tasks in topological order
        for task_name in nx.topological_sort(graph):
            task = graph.nodes[task_name]['task']
            output = execute_task(task, ai_model)
            logging.info(f"Task '{task_name}' completed with output: {output}")

    except Exception as e:
        logging.error(f"Error executing workflow: {e}")
        raise

def main():
    parser = argparse.ArgumentParser(description="AI Task Flow Creator")
    parser.add_argument('--workflow', required=True, help="Path to the workflow YAML or JSON file")
    parser.add_argument('--api-key', required=True, help="OpenAI API key")
    args = parser.parse_args()

    try:
        workflow = load_workflow(args.workflow)
        execute_workflow(workflow, args.api_key)
    except Exception as e:
        logging.error(f"Error: {e}")

if __name__ == "__main__":
    main()
