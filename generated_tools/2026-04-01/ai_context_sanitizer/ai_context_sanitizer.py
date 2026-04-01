import re
import yaml
from argparse import ArgumentParser

def sanitize_prompt(prompt, config=None):
    if config is None:
        config = {}
    # Remove system-level commands
    prompt = re.sub(r'[.;&$`\\]', '', prompt)
    # Remove custom rules
    for rule in config.get('rules', []):
        prompt = re.sub(rule['pattern'], rule['replacement'], prompt)
    return prompt

def load_config(file_path):
    try:
        with open(file_path, 'r') as file:
            return yaml.safe_load(file)
    except FileNotFoundError:
        return {}
    except yaml.YAMLError:
        return {}

if __name__ == '__main__':
    parser = ArgumentParser(description='AI Context Sanitizer')
    parser.add_argument('prompt', help='Raw user input or prompt string')
    parser.add_argument('--config', help='Optional YAML configuration file for custom rules')
    args = parser.parse_args()
    config = load_config(args.config) if args.config else None
    sanitized = sanitize_prompt(args.prompt, config)
    print(sanitized)
