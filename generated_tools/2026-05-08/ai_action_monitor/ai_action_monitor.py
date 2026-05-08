import argparse
import json
import os
import sys
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class ActionMonitorHandler(FileSystemEventHandler):
    def __init__(self, rules, log_file):
        self.rules = rules
        self.log_file = log_file

    def process_action(self, action):
        for rule in self.rules:
            if rule['type'] == action['type'] and rule['operation'] == action['operation']:
                print(f"Flagged risky action: {action}")
                self.log_action(action, flagged=True)
                return
        self.log_action(action, flagged=False)

    def log_action(self, action, flagged):
        log_entry = {
            'action': action,
            'flagged': flagged
        }
        with open(self.log_file, 'a') as f:
            f.write(json.dumps(log_entry) + '\n')

    def on_modified(self, event):
        if event.is_directory:
            return
        try:
            with open(event.src_path, 'r') as f:
                for line in f:
                    try:
                        action = json.loads(line.strip())
                        self.process_action(action)
                    except json.JSONDecodeError:
                        print(f"Invalid JSON format in log: {line.strip()}")
        except Exception as e:
            print(f"Error reading file {event.src_path}: {e}")

def main():
    parser = argparse.ArgumentParser(description="AI Action Monitor")
    parser.add_argument('--log_file', required=True, help="Path to the AI agent action log file")
    parser.add_argument('--rules_file', required=True, help="Path to the JSON ruleset file")
    parser.add_argument('--output_file', required=True, help="Path to the output log file")

    args = parser.parse_args()

    if not os.path.exists(args.log_file):
        print(f"Error: Log file '{args.log_file}' does not exist.")
        sys.exit(1)

    if not os.path.exists(args.rules_file):
        print(f"Error: Rules file '{args.rules_file}' does not exist.")
        sys.exit(1)

    try:
        with open(args.rules_file, 'r') as f:
            rules = json.load(f)
    except json.JSONDecodeError:
        print(f"Error: Rules file '{args.rules_file}' contains invalid JSON.")
        sys.exit(1)
    except Exception as e:
        print(f"Error reading rules file '{args.rules_file}': {e}")
        sys.exit(1)

    event_handler = ActionMonitorHandler(rules, args.output_file)
    observer = Observer()
    observer.schedule(event_handler, path=os.path.dirname(args.log_file) or '.', recursive=False)
    observer.start()

    print("Monitoring AI agent actions. Press Ctrl+C to stop.")
    try:
        while True:
            pass
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

if __name__ == "__main__":
    main()