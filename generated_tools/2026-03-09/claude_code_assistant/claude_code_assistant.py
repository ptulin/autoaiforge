import argparse
import requests
import yaml
import os

def call_claude_api(prompt, api_url, api_key):
    """Call the Claude AI API with the given prompt."""
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json'
    }
    payload = {
        'prompt': prompt,
        'max_tokens': 500
    }
    try:
        response = requests.post(api_url, json=payload, headers=headers)
        response.raise_for_status()
        return response.json().get('response', 'No response from Claude AI.')
    except requests.RequestException as e:
        return f"Error communicating with Claude API: {e}"

def process_input(input_text, api_url, api_key, fix):
    """Process the input text by calling Claude AI for suggestions or fixes."""
    if fix:
        prompt = f"Fix and optimize the following code:\n{input_text}"
    else:
        prompt = f"Provide suggestions for the following code:\n{input_text}"
    return call_claude_api(prompt, api_url, api_key)

def main():
    parser = argparse.ArgumentParser(description="Claude Code Assistant: Get intelligent code suggestions and fixes.")
    parser.add_argument('--file', type=str, help="Path to the input code file.")
    parser.add_argument('--text', type=str, help="Code snippet or error message as input.")
    parser.add_argument('--fix', action='store_true', help="Request fixes and optimizations for the input code.")
    parser.add_argument('--output', type=str, help="Path to save the output suggestions.")
    parser.add_argument('--config', type=str, required=True, help="Path to YAML config file with API details.")

    args = parser.parse_args()

    # Load API configuration
    if not os.path.exists(args.config):
        print("Error: Config file not found.")
        return

    with open(args.config, 'r') as config_file:
        config = yaml.safe_load(config_file)

    api_url = config.get('api_url')
    api_key = config.get('api_key')

    if not api_url or not api_key:
        print("Error: API URL or API key missing in config file.")
        return

    # Read input
    if args.file:
        if not os.path.exists(args.file):
            print("Error: Input file not found.")
            return
        with open(args.file, 'r') as file:
            input_text = file.read()
    elif args.text:
        input_text = args.text
    else:
        print("Error: No input provided. Use --file or --text.")
        return

    # Process input
    result = process_input(input_text, api_url, api_key, args.fix)

    # Output result
    if args.output:
        with open(args.output, 'w') as output_file:
            output_file.write(result)
        print(f"Output saved to {args.output}")
    else:
        print(result)

if __name__ == "__main__":
    main()
