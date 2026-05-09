import numpy as np
import yaml
import json
from tabulate import tabulate
import argparse

def load_configuration(file_path):
    """
    Load the configuration file (YAML or JSON).

    Args:
        file_path (str): Path to the configuration file.

    Returns:
        dict: Parsed configuration data.
    """
    try:
        with open(file_path, 'r') as file:
            if file_path.endswith('.yaml') or file_path.endswith('.yml'):
                return yaml.safe_load(file)
            elif file_path.endswith('.json'):
                return json.load(file)
            else:
                raise ValueError("Unsupported file format. Use YAML or JSON.")
    except FileNotFoundError:
        raise FileNotFoundError(f"Configuration file not found: {file_path}")
    except yaml.YAMLError:
        raise ValueError("Error parsing YAML file.")
    except json.JSONDecodeError:
        raise ValueError("Error parsing JSON file.")

def estimate_cost(config):
    """
    Estimate costs based on the configuration.

    Args:
        config (dict): Configuration data specifying usage patterns.

    Returns:
        dict: Estimated costs and recommendations.
    """
    try:
        models = config.get('models', [])
        recommendations = []

        for model in models:
            name = model.get('name', 'Unknown Model')
            input_size = model.get('input_size', 0)
            output_frequency = model.get('output_frequency', 0)
            usage_hours = model.get('usage_hours', 0)

            # Example cost estimation formula (can be replaced with real-world data)
            cost_per_hour = np.log1p(input_size) * output_frequency * 0.05
            total_cost = cost_per_hour * usage_hours

            # Example recommendation logic
            if total_cost > 100:
                recommendation = "Consider reducing input size or output frequency."
            else:
                recommendation = "Configuration is cost-efficient."

            recommendations.append({
                'Model': name,
                'Total Cost ($)': round(total_cost, 2),
                'Recommendation': recommendation
            })

        return recommendations
    except Exception as e:
        raise ValueError(f"Error in cost estimation: {e}")

def optimize_cost(config_file):
    """
    Optimize cost based on the configuration file.

    Args:
        config_file (str): Path to the configuration file.

    Returns:
        str: Tabulated recommendations and estimated costs.
    """
    config = load_configuration(config_file)
    recommendations = estimate_cost(config)
    return tabulate(recommendations, headers='keys', tablefmt='grid')

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Gemini Cost Optimizer")
    parser.add_argument('config_file', type=str, help="Path to the configuration file (YAML/JSON)")
    args = parser.parse_args()

    try:
        result = optimize_cost(args.config_file)
        print(result)
    except Exception as e:
        print(f"Error: {e}")