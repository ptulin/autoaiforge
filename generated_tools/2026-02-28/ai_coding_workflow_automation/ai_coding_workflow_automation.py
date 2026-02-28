import argparse
import os
import yaml
import requests
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class ConfigError(Exception):
    pass

class AIWorkflowHandler(FileSystemEventHandler):
    def __init__(self, config):
        self.config = config

    def on_modified(self, event):
        if event.is_directory:
            return

        for trigger in self.config['triggers']:
            if trigger['type'] == 'file_change' and event.src_path.endswith(trigger['file']):
                self.handle_trigger(trigger, event.src_path)

    def handle_trigger(self, trigger, file_path):
        try:
            with open(file_path, 'r') as f:
                code_snippet = f.read()
        except FileNotFoundError:
            print(f"File not found: {file_path}")
            return

        payload = {
            'code': code_snippet,
            'instructions': trigger['instructions']
        }

        try:
            response = requests.post(trigger['ai_endpoint'], json=payload)
            response.raise_for_status()
        except requests.RequestException as e:
            print(f"Error communicating with AI endpoint: {e}")
            return

        suggestion = response.json().get('suggestion')
        if suggestion:
            if trigger['action'] == 'save':
                try:
                    with open(file_path, 'w') as f:
                        f.write(suggestion)
                    print(f"Updated {file_path} with AI suggestions.")
                except Exception as e:
                    print(f"Error saving file {file_path}: {e}")
            elif trigger['action'] == 'log':
                print(f"AI suggestion for {file_path}:\n{suggestion}")

class AIWorkflowAutomation:
    def __init__(self, config_path):
        self.config_path = config_path
        self.config = self.load_config()

    def load_config(self):
        if not os.path.exists(self.config_path):
            raise ConfigError(f"Configuration file not found: {self.config_path}")

        with open(self.config_path, 'r') as f:
            try:
                config = yaml.safe_load(f)
            except yaml.YAMLError as e:
                raise ConfigError(f"Error parsing configuration file: {e}")

        if 'triggers' not in config or not isinstance(config['triggers'], list):
            raise ConfigError("Invalid configuration: 'triggers' must be a list.")

        return config

    def start(self):
        event_handler = AIWorkflowHandler(self.config)
        observer = Observer()

        for trigger in self.config['triggers']:
            if trigger['type'] == 'file_change':
                directory = os.path.dirname(trigger['file'])
                observer.schedule(event_handler, directory, recursive=False)

        observer.start()
        print("AI Coding Workflow Automation is running...")

        try:
            while True:
                pass
        except KeyboardInterrupt:
            observer.stop()
        observer.join()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="AI Coding Workflow Automation")
    parser.add_argument('--config', required=True, help="Path to the configuration file")
    args = parser.parse_args()

    try:
        automation = AIWorkflowAutomation(args.config)
        automation.start()
    except ConfigError as e:
        print(f"Configuration error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")