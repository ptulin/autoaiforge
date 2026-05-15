import argparse
import yaml
import schedule
import time
import openai
from datetime import datetime

def load_config(config_path):
    """Load the YAML configuration file."""
    try:
        with open(config_path, 'r') as file:
            return yaml.safe_load(file)
    except FileNotFoundError:
        raise FileNotFoundError(f"Configuration file not found: {config_path}")
    except yaml.YAMLError as e:
        raise ValueError(f"Error parsing YAML file: {e}")

def execute_task(task_name, task_config):
    """Execute a single task based on the configuration."""
    try:
        if 'prompt' not in task_config or 'output_file' not in task_config:
            raise ValueError(f"Task '{task_name}' is missing required fields (prompt, output_file).")

        prompt = task_config['prompt']
        output_file = task_config['output_file']

        # Call the OpenAI API
        response = openai.Completion.create(
            engine=task_config.get('engine', 'text-davinci-003'),
            prompt=prompt,
            max_tokens=task_config.get('max_tokens', 100)
        )

        # Save the output to a file
        with open(output_file, 'w') as f:
            f.write(response['choices'][0]['text'].strip())

        print(f"Task '{task_name}' executed successfully. Output saved to {output_file}.")

    except Exception as e:
        print(f"Error executing task '{task_name}': {e}")

def schedule_tasks(config):
    """Schedule tasks based on the configuration."""
    for task_name, task_config in config.get('tasks', {}).items():
        schedule_type = task_config.get('schedule_type', 'interval')
        interval = task_config.get('interval', 1)

        if schedule_type == 'interval':
            schedule.every(interval).seconds.do(execute_task, task_name, task_config)
        elif schedule_type == 'daily':
            time_str = task_config.get('time', '00:00')
            schedule.every().day.at(time_str).do(execute_task, task_name, task_config)
        else:
            print(f"Unknown schedule type '{schedule_type}' for task '{task_name}'. Skipping.")

def main():
    parser = argparse.ArgumentParser(description="AI Task Scheduler")
    parser.add_argument('--config', required=True, help="Path to the YAML configuration file.")
    args = parser.parse_args()

    try:
        config = load_config(args.config)
        openai.api_key = config.get('api_key')

        if not openai.api_key:
            raise ValueError("OpenAI API key is missing in the configuration file.")

        schedule_tasks(config)

        print("Scheduler started. Press Ctrl+C to exit.")
        while True:
            schedule.run_pending()
            time.sleep(1)

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
