import json
from typing import Dict, Any, List
from pydantic import BaseModel, ValidationError
from cerberus import Validator

class PolicyRule(BaseModel):
    name: str
    condition: Dict[str, Any]
    message: str

class PolicyEnforcer:
    def __init__(self, rules: List[Dict[str, Any]]):
        """
        Initialize the PolicyEnforcer with a list of rules.

        :param rules: List of dictionaries defining policy rules.
        """
        self.rules = []
        for rule in rules:
            try:
                validated_rule = PolicyRule(**rule)
                self.rules.append(validated_rule)
            except ValidationError as e:
                raise ValueError(f"Invalid rule definition: {e}")

    def check(self, action: Dict[str, Any]) -> Dict[str, Any]:
        """
        Check an agent action against the defined rules.

        :param action: Dictionary defining the agent action.
        :return: Compliance report with violations if any.
        """
        validator = Validator()
        violations = []

        for rule in self.rules:
            validator.schema = rule.condition
            if not validator.validate(action):
                violations.append({
                    "rule": rule.name,
                    "message": rule.message,
                    "errors": validator.errors
                })

        return {
            "compliant": len(violations) == 0,
            "violations": violations
        }

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Policy Enforcer CLI")
    parser.add_argument("rules", type=str, help="Path to JSON file containing policy rules")
    parser.add_argument("action", type=str, help="Path to JSON file containing agent action")

    args = parser.parse_args()

    try:
        with open(args.rules, "r") as rules_file:
            rules = json.load(rules_file)

        with open(args.action, "r") as action_file:
            action = json.load(action_file)

        enforcer = PolicyEnforcer(rules)
        result = enforcer.check(action)

        print(json.dumps(result, indent=4))
    except FileNotFoundError as e:
        print(f"Error: {e}")
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON format - {e}")
    except ValueError as e:
        print(f"Error: {e}")
