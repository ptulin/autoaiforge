import argparse
import requests
import json
import yaml
import os

def fetch_memory_data(api_endpoint, api_key, model):
    """
    Fetch memory data from the specified API endpoint.

    Args:
        api_endpoint (str): The API endpoint to fetch memory data from.
        api_key (str): The API key for authentication.
        model (str): The model type (e.g., chatgpt, claude).

    Returns:
        dict: The memory data fetched from the API.

    Raises:
        requests.exceptions.RequestException: If the API request fails.
    """
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    payload = {"model": model}

    response = requests.post(api_endpoint, headers=headers, json=payload)
    response.raise_for_status()
    return response.json()

def export_memory_data(memory_data, output_file, output_format):
    """
    Export memory data to a file in the specified format.

    Args:
        memory_data (dict): The memory data to export.
        output_file (str): The file path to export the data to.
        output_format (str): The format to export the data in (json, yaml, csv).

    Raises:
        ValueError: If the specified format is not supported.
    """
    if output_format == "json":
        with open(output_file, "w") as f:
            json.dump(memory_data, f, indent=4)
    elif output_format == "yaml":
        with open(output_file, "w") as f:
            yaml.dump(memory_data, f, default_flow_style=False)
    else:
        raise ValueError(f"Unsupported output format: {output_format}")

def main():
    parser = argparse.ArgumentParser(description="AI Memory Exporter")
    parser.add_argument("--api_endpoint", required=True, help="API endpoint to fetch memory data from.")
    parser.add_argument("--api_key", required=True, help="API key for authentication.")
    parser.add_argument("--model", required=True, choices=["chatgpt", "claude"], help="Model type (e.g., chatgpt, claude).")
    parser.add_argument("--output", required=True, help="Output file path (e.g., memory.json).")
    parser.add_argument("--format", default="json", choices=["json", "yaml"], help="Output format (default: json).")

    args = parser.parse_args()

    try:
        memory_data = fetch_memory_data(args.api_endpoint, args.api_key, args.model)
        export_memory_data(memory_data, args.output, args.format)
        print(f"Memory data successfully exported to {args.output} in {args.format} format.")
    except requests.exceptions.RequestException as e:
        print(f"Error fetching memory data: {e}")
    except ValueError as e:
        print(f"Error exporting memory data: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()