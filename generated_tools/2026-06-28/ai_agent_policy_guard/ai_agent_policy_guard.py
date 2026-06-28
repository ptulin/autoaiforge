import argparse
import json
import sys
import yaml
import logging
from jsonschema import validate, ValidationError
from colorlog import ColoredFormatter

def setup_logger():
    """Sets up the logger with color formatting."""
    handler = logging.StreamHandler()
    formatter = ColoredFormatter(
        "%(log_color)s%(levelname)s:%(message)s",
        log_colors={
            'DEBUG': 'cyan',
            'INFO': 'green',
            'WARNING': 'yellow',
            'ERROR': 'red',
            'CRITICAL': 'bold_red',
        }
    )
    handler.setFormatter(formatter)
    logger = logging.getLogger("policy_guard")
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)
    return logger

def load_policy(policy_path, logger):
    """Loads the policy file (YAML or JSON)."""
    try:
        with open(policy_path, 'r') as file:
            if policy_path.endswith('.yaml') or policy_path.endswith('.yml'):
                return yaml.safe_load(file)
            elif policy_path.endswith('.json'):
                return json.load(file)
            else:
                raise ValueError("Unsupported policy file format. Use YAML or JSON.")
    except Exception as e:
        logger.error(f"Failed to load policy file: {e}")
        sys.exit(1)

def validate_policy(policy, logger):
    """Validates the policy structure."""
    schema = {
        "type": "object",
        "properties": {
            "rules": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "pattern": {"type": "string"},
                        "action": {"type": "string", "enum": ["log", "alert", "halt"]}
                    },
                    "required": ["pattern", "action"]
                }
            }
        },
        "required": ["rules"]
    }
    try:
        validate(instance=policy, schema=schema)
    except ValidationError as e:
        logger.error(f"Policy validation error: {e.message}")
        sys.exit(1)

def monitor_logs(policy, log_stream, logger):
    """Monitors the log stream and enforces policy rules."""
    for line in log_stream:
        line = line.strip()
        for rule in policy['rules']:
            if rule['pattern'] in line:
                action = rule['action']
                if action == 'log':
                    logger.warning(f"Policy violation logged: {line}")
                elif action == 'alert':
                    logger.error(f"Policy violation alert: {line}")
                elif action == 'halt':
                    logger.critical(f"Policy violation detected. Halting: {line}")
                    sys.exit(1)

def main():
    parser = argparse.ArgumentParser(
        description="AI Agent Policy Guard: Monitor and enforce behavior policies for AI agents."
    )
    parser.add_argument('--policy', required=True, help="Path to the policy file (YAML or JSON).")
    parser.add_argument('--log', required=True, help="Path to the log file or '-' for stdin.")
    args = parser.parse_args()

    logger = setup_logger()

    policy = load_policy(args.policy, logger)
    validate_policy(policy, logger)

    if args.log == '-':
        log_stream = sys.stdin
    else:
        try:
            log_stream = open(args.log, 'r')
        except Exception as e:
            logger.error(f"Failed to open log file: {e}")
            sys.exit(1)

    try:
        monitor_logs(policy, log_stream, logger)
    finally:
        if args.log != '-':
            log_stream.close()

if __name__ == "__main__":
    main()
