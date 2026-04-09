import argparse
import json
import time
import httpx

def send_request(endpoint, payload):
    """Send a POST request to the specified endpoint with the given payload."""
    try:
        start_time = time.time()
        response = httpx.post(endpoint, json=payload, timeout=10)
        response_time = time.time() - start_time
        response.raise_for_status()
        return response.json(), response_time
    except httpx.RequestError as e:
        return {"error": str(e)}, None

def validate_response(response, expected):
    """Validate the response against the expected output."""
    return response == expected

def main():
    parser = argparse.ArgumentParser(description="Claude API Tester")
    parser.add_argument("--endpoint", required=True, help="API endpoint URL")
    parser.add_argument("--payload", required=True, help="Path to the JSON file containing the request payload")
    parser.add_argument("--expected", help="Path to the JSON file containing the expected response")
    parser.add_argument("--output", help="Path to save the results")

    args = parser.parse_args()

    try:
        with open(args.payload, "r") as f:
            payload = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error reading payload file: {e}")
        return

    expected = None
    if args.expected:
        try:
            with open(args.expected, "r") as f:
                expected = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Error reading expected file: {e}")
            return

    response, response_time = send_request(args.endpoint, payload)

    if response_time is not None:
        print(f"Response time: {response_time:.2f} seconds")
    else:
        print("Failed to get a valid response.")

    if "error" in response:
        print(f"Error: {response['error']}")
    else:
        print("Response:", json.dumps(response, indent=2))

        if expected:
            is_valid = validate_response(response, expected)
            print("Validation result:", "Pass" if is_valid else "Fail")

    if args.output:
        try:
            with open(args.output, "w") as f:
                json.dump({"response": response, "response_time": response_time}, f, indent=2)
            print(f"Results saved to {args.output}")
        except Exception as e:
            print(f"Error saving results: {e}")

if __name__ == "__main__":
    main()
