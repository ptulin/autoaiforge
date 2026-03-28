import argparse
import requests
import os

def fetch_optimized_tests(api_key, code_content):
    """
    Fetch optimized test cases from Claude AI API.

    Args:
        api_key (str): Claude API key.
        code_content (str): Python code content to analyze.

    Returns:
        str: Generated pytest-compatible test cases.
    """
    url = "https://api.claude.ai/v1/optimize-tests"
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    payload = {"code": code_content}

    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        return response.json().get("optimized_tests", "")
    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"Failed to fetch optimized tests: {e}")

def read_file(file_path):
    """
    Read content from a file.

    Args:
        file_path (str): Path to the file.

    Returns:
        str: File content.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    with open(file_path, "r") as file:
        return file.read()

def write_file(file_path, content):
    """
    Write content to a file.

    Args:
        file_path (str): Path to the file.
        content (str): Content to write.
    """
    with open(file_path, "w") as file:
        file.write(content)

def main():
    parser = argparse.ArgumentParser(description="Claude Test Suite Optimizer")
    parser.add_argument("--code", required=True, help="Path to the Python code file")
    parser.add_argument("--api-key", required=True, help="Claude API key")
    parser.add_argument("--output", default="optimized_tests.py", help="Output file for optimized tests")

    args = parser.parse_args()

    try:
        code_content = read_file(args.code)
        optimized_tests = fetch_optimized_tests(args.api_key, code_content)

        if not optimized_tests:
            print("No optimized tests were generated.")
            return

        write_file(args.output, optimized_tests)
        print(f"Optimized tests written to {args.output}")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()