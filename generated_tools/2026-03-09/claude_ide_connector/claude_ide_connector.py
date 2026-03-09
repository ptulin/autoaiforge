import requests
import jedi
from rich.console import Console

class ClaudeAPIError(Exception):
    """Custom exception for Claude API errors."""
    pass

class Client:
    def __init__(self, api_key: str, base_url: str = "https://api.claude.ai/v1"):
        """
        Initialize the Claude IDE Connector client.

        :param api_key: API key for authenticating with the Claude AI service.
        :param base_url: Base URL for the Claude API (default: https://api.claude.ai/v1).
        """
        self.api_key = api_key
        self.base_url = base_url
        self.console = Console()

    def _post_request(self, endpoint: str, payload: dict) -> dict:
        """
        Internal method to send a POST request to the Claude API.

        :param endpoint: API endpoint to send the request to.
        :param payload: JSON payload for the request.
        :return: JSON response from the API.
        """
        url = f"{self.base_url}/{endpoint}"
        headers = {"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"}

        try:
            response = requests.post(url, json=payload, headers=headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise ClaudeAPIError(f"Error communicating with Claude API: {e}")

    def get_suggestions(self, code: str) -> dict:
        """
        Get code suggestions from Claude AI.

        :param code: Code context to send to Claude AI.
        :return: Suggestions, fixes, or optimizations from Claude AI.
        """
        if not code.strip():
            raise ValueError("Code input cannot be empty.")

        payload = {"code": code}
        return self._post_request("suggestions", payload)

    def analyze_code(self, code: str) -> dict:
        """
        Analyze the given code for errors and optimization hints.

        :param code: Code to analyze.
        :return: Analysis results from Claude AI.
        """
        if not code.strip():
            raise ValueError("Code input cannot be empty.")

        payload = {"code": code}
        return self._post_request("analyze", payload)

    def inline_completion(self, code: str, cursor_position: int) -> dict:
        """
        Get inline code completion suggestions from Claude AI.

        :param code: Code context to send to Claude AI.
        :param cursor_position: Position of the cursor in the code.
        :return: Inline code completion suggestions.
        """
        if not code.strip():
            raise ValueError("Code input cannot be empty.")

        payload = {"code": code, "cursor_position": cursor_position}
        return self._post_request("completion", payload)

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Claude IDE Connector CLI")
    parser.add_argument("api_key", help="Your Claude AI API key")
    parser.add_argument("code", help="Code to analyze or get suggestions for")
    parser.add_argument("--analyze", action="store_true", help="Analyze the code for errors and optimizations")
    parser.add_argument("--suggest", action="store_true", help="Get code suggestions")
    parser.add_argument("--complete", type=int, help="Get inline completion at the given cursor position")

    args = parser.parse_args()

    client = Client(api_key=args.api_key)

    if args.analyze:
        result = client.analyze_code(args.code)
        client.console.print(result)
    elif args.suggest:
        result = client.get_suggestions(args.code)
        client.console.print(result)
    elif args.complete is not None:
        result = client.inline_completion(args.code, args.complete)
        client.console.print(result)
    else:
        parser.print_help()
