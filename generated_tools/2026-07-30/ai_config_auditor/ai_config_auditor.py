import argparse
import json
import yaml
import configparser
import openai
import os

def analyze_configuration(config_content, config_format):
    """
    Analyze the configuration content using OpenAI API to identify misconfigurations.

    Args:
        config_content (str): The content of the configuration file as a string.
        config_format (str): The format of the configuration file (e.g., 'yaml', 'json', 'ini').

    Returns:
        dict: A dictionary containing analysis results and recommendations.
    """
    try:
        prompt = (
            f"Analyze the following {config_format.upper()} configuration file for security misconfigurations. "
            "Provide a detailed report with identified issues and remediation recommendations:\n\n"
            f"{config_content}"
        )

        # Call OpenAI API
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=500
        )

        return {
            "success": True,
            "analysis": response.choices[0].text.strip()
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

def load_configuration(file_path):
    """
    Load the configuration file based on its format.

    Args:
        file_path (str): Path to the configuration file.

    Returns:
        tuple: A tuple containing the file content as a string and its format.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Configuration file '{file_path}' not found.")

    _, ext = os.path.splitext(file_path)
    ext = ext.lower()

    with open(file_path, 'r') as file:
        if ext == '.yaml' or ext == '.yml':
            return file.read(), 'yaml'
        elif ext == '.json':
            return file.read(), 'json'
        elif ext == '.ini':
            return file.read(), 'ini'
        else:
            raise ValueError(f"Unsupported configuration file format: {ext}")

def main():
    parser = argparse.ArgumentParser(description="AI Configuration Auditor")
    parser.add_argument(
        '--config',
        required=True,
        help="Path to the configuration file (YAML, JSON, or INI)."
    )

    args = parser.parse_args()

    try:
        config_content, config_format = load_configuration(args.config)
        result = analyze_configuration(config_content, config_format)

        if result["success"]:
            print("\nAnalysis Report:\n")
            print(result["analysis"])
        else:
            print(f"Error during analysis: {result['error']}")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()