import json
import yaml
from jsonschema import validate, ValidationError

class PolicyMapper:
    """
    AI Policy Mapper

    This class provides functionality to map AI system features to global ethical AI policies.
    """

    @staticmethod
    def load_policy(file_path):
        """
        Load a policy file in YAML format.

        Args:
            file_path (str): Path to the policy file.

        Returns:
            dict: Parsed policy data.

        Raises:
            FileNotFoundError: If the file does not exist.
            yaml.YAMLError: If the file is not a valid YAML.
        """
        try:
            with open(file_path, 'r') as file:
                return yaml.safe_load(file)
        except FileNotFoundError:
            raise FileNotFoundError(f"Policy file '{file_path}' not found.")
        except yaml.YAMLError as e:
            raise ValueError(f"Error parsing YAML file: {e}")

    @staticmethod
    def match_features_to_policies(features, policy_file):
        """
        Match AI system features to a policy.

        Args:
            features (dict): Dictionary describing AI system features.
            policy_file (str): Path to the policy file.

        Returns:
            list: List of compliance gaps or mismatches.

        Raises:
            ValidationError: If the features do not comply with the policy schema.
        """
        try:
            policy = PolicyMapper.load_policy(policy_file)
            schema = policy.get("schema")
            if not schema:
                raise ValueError("Policy file does not contain a valid schema.")

            validate(instance=features, schema=schema)
            return []  # No compliance gaps
        except ValidationError as e:
            return [str(e)]
        except Exception as e:
            return [f"Error: {e}"]

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="AI Policy Mapper: Map AI features to ethical AI policies.")
    parser.add_argument("features", type=str, help="Path to the JSON file describing AI system features.")
    parser.add_argument("policy", type=str, help="Path to the YAML file containing the policy schema.")

    args = parser.parse_args()

    try:
        with open(args.features, 'r') as f:
            features = json.load(f)

        gaps = PolicyMapper.match_features_to_policies(features, args.policy)

        if gaps:
            print("Compliance gaps found:")
            for gap in gaps:
                print(f"- {gap}")
        else:
            print("The AI system complies with the policy.")
    except Exception as e:
        print(f"Error: {e}")