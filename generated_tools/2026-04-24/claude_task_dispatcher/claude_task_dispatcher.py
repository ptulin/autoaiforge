import os
import sys
import json
import yaml
import logging
import requests
import schedule
import time
import argparse
from datetime import datetime

def load_workflow(file_path):
    """Load workflow from a JSON or YAML file."""
    try:
        with open(file_path, 'r') as f:
            if file_path.endswith('.json'):
                return json.load(f)
            elif file_path.endswith('.yml') or file_path.endswith('.yaml'):
                return yaml.safe_load(f)
            else:
                raise ValueError("Unsupported file format. Use JSON or YAML.")
    except Exception as e:
        logging.error(f"Failed to load workflow file: {e}")
        sys.exit(1)

def execute_task(task):
    """Execute a single task."""
    try:
        if task['type'] == 'http_request':
            response = requests.request(
                method=task['method'],
                url=task['url'],
                headers=task.get('headers', {}),
                json=task.get('body', {})
            )
            logging.info(f"Task executed: {task['name']} - Status: {response.status_code}")
        else:
            logging.warning(f"Unsupported task type: {task['type']}")
    except Exception as e:
        logging.error(f"Error executing task {task['name']}: {e}")

def execute_workflow(workflow):
    """Execute all tasks in the workflow."""
    logging.info(f"Starting workflow: {workflow['name']}")
    for task in workflow['tasks']:
        execute_task(task)
    logging.info(f"Workflow completed: {workflow['name']}")

def schedule_workflow(workflow, cron_expression):
    """Schedule a workflow based on a cron-like expression."""
    def job():
        execute_workflow(workflow)

    try:
        schedule.every().minute.at(cron_expression).do(job)
        logging.info(f"Workflow scheduled: {workflow['name']} with cron: {cron_expression}")

        while True:
            schedule.run_pending()
            time.sleep(1)
    except Exception as e:
        logging.error(f"Error scheduling workflow: {e}")
        sys.exit(1)

def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(description="Claude Task Dispatcher")
    parser.add_argument('--workflow', required=True, type=str, help='Path to the workflow file (JSON or YAML).')
    parser.add_argument('--schedule', type=str, default=None, help='Cron-like schedule expression (e.g., "/15 * * * *").')
    parser.add_argument('--execute', action='store_true', help='Immediately execute the workflow.')

    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    workflow_data = load_workflow(args.workflow)

    if args.execute:
        execute_workflow(workflow_data)
    elif args.schedule:
        schedule_workflow(workflow_data, args.schedule)
    else:
        logging.error("Either --execute or --schedule must be specified.")
        sys.exit(1)

if __name__ == '__main__':
    main()
