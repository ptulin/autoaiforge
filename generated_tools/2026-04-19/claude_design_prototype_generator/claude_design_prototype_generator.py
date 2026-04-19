import os
import argparse
import requests
import json

def generate_prototype(api_key, prompt, output_format, output_file):
    """
    Generate a UI/UX prototype using the Claude Design API.

    Args:
        api_key (str): The API key for authenticating with the Claude Design API.
        prompt (str): The text prompt describing the design.
        output_format (str): The desired output format (json or png).
        output_file (str): The file path to save the generated prototype.

    Returns:
        str: The path to the saved prototype file.

    Raises:
        ValueError: If the output format is invalid.
        Exception: If the API request fails.
    """
    if output_format not in ["json", "png"]:
        raise ValueError("Invalid output format. Supported formats are 'json' and 'png'.")

    url = "https://api.anthropic.com/v1/design/prototype"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    payload = {
        "prompt": prompt,
        "output_format": output_format
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
    except requests.RequestException as e:
        raise Exception(f"Failed to connect to the API: {e}")

    try:
        with open(output_file, "wb") as f:
            f.write(response.content)
    except Exception as e:
        raise Exception(f"Failed to save the prototype file: {e}")

    return output_file

def main():
    parser = argparse.ArgumentParser(description="Claude Design Prototype Generator")
    parser.add_argument("--prompt", required=True, help="Text prompt describing the design")
    parser.add_argument("--output-format", required=True, choices=["json", "png"], help="Output format (json or png)")
    parser.add_argument("--output-file", required=True, help="Path to save the generated prototype")

    args = parser.parse_args()

    api_key = os.getenv("CLAUDE_API_KEY")
    if not api_key:
        print("Error: CLAUDE_API_KEY environment variable is not set.")
        exit(1)

    try:
        output_path = generate_prototype(api_key, args.prompt, args.output_format, args.output_file)
        print(f"Prototype successfully generated and saved to {output_path}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()