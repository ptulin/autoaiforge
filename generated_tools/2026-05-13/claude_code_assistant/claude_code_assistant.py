import requests
import argparse
from typing import Union

class ClaudeCodeAssistant:
    """
    Claude Code Assistant: A library to enhance coding workflows using Claude AI.
    """

    def __init__(self, api_key: str):
        if not api_key:
            raise ValueError("API key is required to use Claude Code Assistant.")
        self.api_key = api_key
        self.api_url = "https://api.openai.com/v1/completions"

    def suggest_code(self, prompt: str) -> str:
        """
        Suggest code snippets based on the provided prompt.

        Args:
            prompt (str): A description of the coding problem or task.

        Returns:
            str: AI-generated code suggestion.
        """
        if not prompt.strip():
            raise ValueError("Prompt cannot be empty.")

        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            data = {
                "model": "text-davinci-003",
                "prompt": prompt,
                "max_tokens": 150,
                "temperature": 0.7
            }
            response = requests.post(self.api_url, headers=headers, json=data)
            response.raise_for_status()
            result = response.json()
            return result.get("choices", [{}])[0].get("text", "No suggestion available.").strip()
        except requests.RequestException as e:
            return f"Error communicating with Claude API: {e}"

    def debug_code(self, code_snippet: str) -> str:
        """
        Provide debugging insights for a given code snippet.

        Args:
            code_snippet (str): The code snippet to debug.

        Returns:
            str: AI-generated debugging insights.
        """
        if not code_snippet.strip():
            raise ValueError("Code snippet cannot be empty.")

        prompt = f"Debug the following Python code:\n{code_snippet}"
        return self.suggest_code(prompt)

    def refactor_code(self, code_snippet: str) -> str:
        """
        Refactor and optimize the provided code snippet.

        Args:
            code_snippet (str): The code snippet to refactor.

        Returns:
            str: AI-generated refactored code.
        """
        if not code_snippet.strip():
            raise ValueError("Code snippet cannot be empty.")

        prompt = f"Refactor and optimize the following Python code:\n{code_snippet}"
        return self.suggest_code(prompt)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Claude Code Assistant CLI")
    parser.add_argument("--api_key", required=True, help="Your Claude API key.")
    parser.add_argument("--action", required=True, choices=["suggest", "debug", "refactor"], help="Action to perform: suggest, debug, or refactor.")
    parser.add_argument("--input", required=True, help="Input prompt or code snippet.")

    args = parser.parse_args()

    assistant = ClaudeCodeAssistant(api_key=args.api_key)

    if args.action == "suggest":
        print(assistant.suggest_code(args.input))
    elif args.action == "debug":
        print(assistant.debug_code(args.input))
    elif args.action == "refactor":
        print(assistant.refactor_code(args.input))