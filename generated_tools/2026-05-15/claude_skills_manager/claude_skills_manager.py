import argparse
import yaml
import requests
import os

def validate_skill_config(skill_config):
    """Validate the structure of the skill configuration."""
    required_keys = ["name", "description", "triggers", "actions"]
    for key in required_keys:
        if key not in skill_config:
            raise ValueError(f"Missing required key: {key}")
    return True

def load_skill_config(file_path):
    """Load a skill configuration from a YAML file."""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")
    with open(file_path, 'r') as file:
        return yaml.safe_load(file)

def deploy_skill(skill_config, api_url):
    """Deploy the skill configuration to the Claude API."""
    try:
        response = requests.post(f"{api_url}/deploy", json=skill_config)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        raise ConnectionError(f"Failed to deploy skill: {e}")

def main():
    parser = argparse.ArgumentParser(description="Claude Skills Manager")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Subparser for the 'validate' command
    validate_parser = subparsers.add_parser("validate", help="Validate a skill configuration YAML file.")
    validate_parser.add_argument("--skill", required=True, help="Path to the skill YAML file.")

    # Subparser for the 'deploy' command
    deploy_parser = subparsers.add_parser("deploy", help="Deploy a skill configuration to Claude AI.")
    deploy_parser.add_argument("--skill", required=True, help="Path to the skill YAML file.")
    deploy_parser.add_argument("--api-url", required=True, help="Claude API base URL.")

    args = parser.parse_args()

    try:
        if args.command == "validate":
            skill_config = load_skill_config(args.skill)
            validate_skill_config(skill_config)
            print("Skill configuration is valid.")

        elif args.command == "deploy":
            skill_config = load_skill_config(args.skill)
            validate_skill_config(skill_config)
            result = deploy_skill(skill_config, args.api_url)
            print("Skill deployed successfully:", result)

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()