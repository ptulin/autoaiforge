import argparse
import openai
import yaml
import os

def generate_workflow(prompt, platform, api_key):
    """
    Generates a CI/CD workflow YAML configuration based on a natural language prompt.

    Args:
        prompt (str): The natural language description of the desired workflow.
        platform (str): The target platform (e.g., 'github', 'gitlab').
        api_key (str): OpenAI API key for accessing GPT models.

    Returns:
        str: The generated YAML configuration as a string.

    Raises:
        ValueError: If the platform is unsupported.
        Exception: If an error occurs during the OpenAI API call.
    """
    if platform not in ['github', 'gitlab']:
        raise ValueError("Unsupported platform. Supported platforms are: 'github', 'gitlab'.")

    openai.api_key = api_key

    try:
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=f"Generate a {platform} CI/CD workflow YAML file for the following task: {prompt}",
            max_tokens=500
        )
        yaml_content = response.choices[0].text.strip()

        # Validate YAML syntax
        yaml.safe_load(yaml_content)

        return yaml_content
    except yaml.YAMLError as e:
        raise ValueError("Generated YAML is invalid.") from e
    except Exception as e:
        raise Exception("Failed to generate workflow.") from e

def save_workflow_to_file(yaml_content, output_file):
    """
    Saves the generated YAML content to a file.

    Args:
        yaml_content (str): The YAML content to save.
        output_file (str): The output file path.
    """
    with open(output_file, 'w') as file:
        file.write(yaml_content)

def main():
    parser = argparse.ArgumentParser(description="Workflow Auto-Generator: Generate CI/CD workflows from natural language prompts.")
    parser.add_argument('--prompt', required=True, help="Natural language description of the desired workflow.")
    parser.add_argument('--platform', required=True, choices=['github', 'gitlab'], help="Target platform for the workflow (github or gitlab).")
    parser.add_argument('--output', required=True, help="Output file to save the generated workflow YAML.")
    parser.add_argument('--api-key', required=True, help="OpenAI API key.")

    args = parser.parse_args()

    try:
        yaml_content = generate_workflow(args.prompt, args.platform, args.api_key)
        save_workflow_to_file(yaml_content, args.output)
        print(f"Workflow successfully generated and saved to {args.output}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()