import argparse
import json
import logging
import os
import subprocess
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class ConfigLoader:
    def __init__(self, config_path):
        self.config_path = config_path
        self.config = None

    def load_config(self):
        if not os.path.exists(self.config_path):
            raise FileNotFoundError(f"Configuration file not found: {self.config_path}")
        with open(self.config_path, 'r') as file:
            self.config = json.load(file)
        return self.config

class CommandExecutor:
    def __init__(self, allowed_commands, logger):
        self.allowed_commands = allowed_commands
        self.logger = logger

    def execute(self, command):
        if command not in self.allowed_commands:
            self.logger.warning(f"Blocked unauthorized command: {command}")
            return f"Command '{command}' is not allowed."

        try:
            result = subprocess.run(command, shell=True, capture_output=True, text=True)
            self.logger.info(f"Executed command: {command}, Return code: {result.returncode}, Output: {result.stdout.strip()}")
            return result.stdout.strip()
        except Exception as e:
            self.logger.error(f"Error executing command '{command}': {e}")
            return f"Error executing command: {e}"

class TaskHandler(FileSystemEventHandler):
    def __init__(self, config_loader, executor):
        self.config_loader = config_loader
        self.executor = executor

    def on_modified(self, event):
        if event.src_path == self.config_loader.config_path:
            self.config_loader.load_config()
            self.executor.logger.info("Configuration file reloaded.")

    def handle_tasks(self):
        tasks = self.config_loader.config.get("tasks", [])
        for task in tasks:
            command = task.get("command")
            if command:
                self.executor.execute(command)

class AISystemGuardian:
    def __init__(self, config_path):
        self.config_loader = ConfigLoader(config_path)
        self.config = self.config_loader.load_config()
        self.logger = self.setup_logger()
        self.executor = CommandExecutor(self.config.get("allowed_commands", []), self.logger)
        self.task_handler = TaskHandler(self.config_loader, self.executor)

    def setup_logger(self):
        log_file = self.config.get("log_file", "ai_system_guardian.log")
        logging.basicConfig(
            filename=log_file,
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        return logging.getLogger("AISystemGuardian")

    def start(self):
        observer = Observer()
        observer.schedule(self.task_handler, path=os.path.dirname(self.config_loader.config_path) or '.', recursive=False)
        observer.start()
        try:
            self.task_handler.handle_tasks()
            while True:
                pass
        except KeyboardInterrupt:
            observer.stop()
        observer.join()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="AI System Guardian: Secure wrapper for monitoring AI agent actions.")
    parser.add_argument("--config", required=True, help="Path to the JSON configuration file.")
    args = parser.parse_args()

    guardian = AISystemGuardian(args.config)
    guardian.start()