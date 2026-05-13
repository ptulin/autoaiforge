import argparse
import json
import requests

def query_memory(api_url, key):
    try:
        response = requests.get(f"{api_url}/memory", params={"key": key})
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}

def add_memory(api_url, key, value):
    try:
        payload = {"key": key, "value": value}
        response = requests.post(f"{api_url}/memory", json=payload)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}

def delete_memory(api_url, key):
    try:
        response = requests.delete(f"{api_url}/memory", params={"key": key})
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}

def main():
    parser = argparse.ArgumentParser(description="Claude Memory Manager")
    parser.add_argument("--api-url", required=True, help="Base URL of the Claude API")
    parser.add_argument("--query", help="Query memory by key")
    parser.add_argument("--add", nargs=2, metavar=("KEY", "VALUE"), help="Add or update memory with key and value")
    parser.add_argument("--delete", help="Delete memory by key")

    args = parser.parse_args()

    if args.query:
        result = query_memory(args.api_url, args.query)
    elif args.add:
        key, value = args.add
        result = add_memory(args.api_url, key, value)
    elif args.delete:
        result = delete_memory(args.api_url, args.delete)
    else:
        result = {"error": "No valid operation specified"}

    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    main()