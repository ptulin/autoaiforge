import json
import yaml
import schedule
import time
import requests
from loguru import logger
import click
from datetime import datetime
from pathlib import Path

class TaskScheduler:
    def __init__(self, config_path):
        self.tasks = []
        self.load_config(config_path)

    def load_config(self, config_path):
        try:
            config_path = str(config_path)  # Ensure the path is a string
            with open(config_path, 'r') as file:
                if config_path.endswith('.json'):
                    config = json.load(file)
                elif config_path.endswith('.yaml') or config_path.endswith('.yml'):
                    config = yaml.safe_load(file)
                else:
                    raise ValueError("Unsupported file format. Use JSON or YAML.")

            self.tasks = config.get('tasks', [])
            logger.info(f"Loaded {len(self.tasks)} tasks from configuration.")
        except Exception as e:
            logger.error(f"Failed to load configuration: {e}")
            raise

    def execute_task(self, task):
        try:
            logger.info(f"Executing task: {task['name']}")
            if task['type'] == 'api_request':
                response = requests.request(
                    method=task['method'],
                    url=task['url'],
                    headers=task.get('headers', {}),
                    json=task.get('payload', {})
                )
                logger.info(f"Task {task['name']} completed with status {response.status_code}: {response.text}")
            elif task['type'] == 'custom_script':
                exec(task['script'])
                logger.info(f"Task {task['name']} custom script executed successfully.")
            else:
                logger.warning(f"Unknown task type: {task['type']}")
        except Exception as e:
            logger.error(f"Error executing task {task['name']}: {e}")

    def schedule_tasks(self):
        for task in self.tasks:
            trigger = task.get('trigger')
            if not trigger:
                logger.warning(f"Task {task['name']} has no trigger defined. Skipping.")
                continue

            if 'cron' in trigger:
                cron = trigger['cron']
                hour, minute = map(int, cron.split(':'))
                schedule.every().day.at(f"{hour:02}:{minute:02}").do(self.execute_task, task)
                logger.info(f"Scheduled task {task['name']} with cron: {cron}")
            else:
                logger.warning(f"Unsupported trigger type for task {task['name']}. Skipping.")

    def run(self):
        logger.info("Starting task scheduler...")
        while True:
            schedule.run_pending()
            time.sleep(1)

@click.command()
@click.option('--config', '-c', required=True, type=click.Path(exists=True, path_type=Path), help='Path to the configuration file (JSON or YAML).')
def main(config):
    """Smart Task Scheduler: Schedule and execute tasks using a configuration file."""
    logger.add("scheduler_{time}.log", rotation="1 day", retention="7 days")
    try:
        scheduler = TaskScheduler(config)
        scheduler.schedule_tasks()
        scheduler.run()
    except Exception as e:
        logger.error(f"Scheduler failed: {e}")

if __name__ == "__main__":
    main()
