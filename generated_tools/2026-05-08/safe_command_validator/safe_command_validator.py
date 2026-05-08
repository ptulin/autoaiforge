import re
import json
import logging
from typing import List

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger("SafeCommandValidator")

def validate_command(command: str, rules_file: str) -> bool:
    """
    Validates a command string against a whitelist or blacklist defined in a JSON file.

    Args:
        command (str): The command string to validate.
        rules_file (str): Path to the JSON file containing whitelist/blacklist rules.

    Returns:
        bool: True if the command is safe, False otherwise.
    """
    try:
        # Load rules from the JSON file
        with open(rules_file, 'r') as file:
            rules = json.load(file)

        whitelist = rules.get("whitelist", [])
        blacklist = rules.get("blacklist", [])

        # Validate against blacklist
        for pattern in blacklist:
            if re.search(pattern, command):
                logger.warning(f"Command rejected by blacklist: {command}")
                return False

        # Validate against whitelist (if provided)
        if whitelist:
            for pattern in whitelist:
                if re.search(pattern, command):
                    return True
            logger.warning(f"Command rejected by whitelist: {command}")
            return False

        # If no whitelist is provided, and not blacklisted, allow the command
        return True

    except FileNotFoundError:
        logger.error(f"Rules file not found: {rules_file}")
        return False
    except json.JSONDecodeError:
        logger.error(f"Invalid JSON format in rules file: {rules_file}")
        return False
    except Exception as e:
        logger.error(f"Unexpected error during command validation: {e}")
        return False

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Safe Command Validator")
    parser.add_argument("command", type=str, help="The command string to validate.")
    parser.add_argument("rules_file", type=str, help="Path to the JSON file containing whitelist/blacklist rules.")

    args = parser.parse_args()

    if validate_command(args.command, args.rules_file):
        print("Command is safe.")
    else:
        print("Command is rejected.")