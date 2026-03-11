import argparse
import json
import yaml
import os
import requests

def save_memory(api_url, api_key, memory_data):
    """Saves memory data to Claude AI."""
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    try:
        response = requests.post(f"{api_url}/memory", headers=headers, json=memory_data)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        raise RuntimeError(f"Failed to save memory: {e}")

def retrieve_memory(api_url, api_key):
    """Retrieves memory data from Claude AI."""
    headers = {"Authorization": f"Bearer {api_key}"}
    try:
        response = requests.get(f"{api_url}/memory", headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        raise RuntimeError(f"Failed to retrieve memory: {e}")

def delete_memory(api_url, api_key, memory_id):
    """Deletes a specific memory entry from Claude AI."""
    headers = {"Authorization": f"Bearer {api_key}"}
    try:
        response = requests.delete(f"{api_url}/memory/{memory_id}", headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        raise RuntimeError(f"Failed to delete memory: {e}")

def load_data(file_path):
    """Loads data from a JSON or YAML file."""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    with open(file_path, 'r') as file:
        if file_path.endswith('.json'):
            return json.load(file)
        elif file_path.endswith('.yaml') or file_path.endswith('.yml'):
            return yaml.safe_load(file)
        else:
            raise ValueError("Unsupported file format. Use JSON or YAML.")

def main():
    parser = argparse.ArgumentParser(description="Claude Memory Manager")
    parser.add_argument("--api-url", required=True, help="Claude AI API URL")
    parser.add_argument("--api-key", required=True, help="Claude AI API Key")
    parser.add_argument("--save", help="Path to JSON or YAML file to save memory data")
    parser.add_argument("--retrieve", action="store_true", help="Retrieve memory data")
    parser.add_argument("--delete", help="ID of the memory entry to delete")
    parser.add_argument("--output", help="Path to save retrieved memory data (optional)")

    args = parser.parse_args()

    try:
        if args.save:
            memory_data = load_data(args.save)
            result = save_memory(args.api_url, args.api_key, memory_data)
            print("Memory saved successfully:", result)

        elif args.retrieve:
            result = retrieve_memory(args.api_url, args.api_key)
            if args.output:
                with open(args.output, 'w') as file:
                    json.dump(result, file, indent=4)
                print(f"Memory retrieved and saved to {args.output}")
            else:
                print("Retrieved memory:", json.dumps(result, indent=4))

        elif args.delete:
            result = delete_memory(args.api_url, args.api_key, args.delete)
            print("Memory deleted successfully:", result)

        else:
            parser.print_help()

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()