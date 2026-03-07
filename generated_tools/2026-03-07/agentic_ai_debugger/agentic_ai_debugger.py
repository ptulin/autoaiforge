import argparse
import os
import openai
from rich.console import Console
from rich.table import Table

console = Console()

class AgenticAIDebugger:
    def __init__(self, api_key, auto_apply=False):
        self.api_key = api_key
        self.auto_apply = auto_apply
        openai.api_key = self.api_key

    def analyze_code(self, code, error_message):
        """Analyze the code and error message using OpenAI API."""
        prompt = f"""
        You are an expert Python developer. Analyze the following code and error message. Suggest fixes and explain them clearly.

        Code:
        {code}

        Error Message:
        {error_message}
        """
        try:
            response = openai.Completion.create(
                engine="text-davinci-003",
                prompt=prompt,
                max_tokens=500
            )
            return response["choices"][0]["text"].strip()
        except Exception as e:
            console.print(f"[red]Error communicating with OpenAI API: {e}")
            return None

    def apply_fix(self, file_path, fix):
        """Apply the suggested fix to the file."""
        try:
            with open(file_path, "r") as file:
                original_code = file.read()

            fixed_code = original_code + "\n\n# Suggested Fix:\n" + fix

            with open(file_path, "w") as file:
                file.write(fixed_code)

            console.print(f"[green]Fix applied to {file_path}")
        except Exception as e:
            console.print(f"[red]Error applying fix: {e}")

    def process_file(self, file_path, error_message):
        """Process a single Python file."""
        if not os.path.isfile(file_path):
            console.print(f"[red]File not found: {file_path}")
            return

        try:
            with open(file_path, "r") as file:
                code = file.read()

            suggestions = self.analyze_code(code, error_message)
            if suggestions:
                console.print("\n[bold]Suggestions:[/bold]")
                console.print(suggestions)

                if self.auto_apply:
                    self.apply_fix(file_path, suggestions)
        except Exception as e:
            console.print(f"[red]Error processing file: {e}")

    def process_directory(self, directory, error_message):
        """Process all Python files in a directory."""
        if not os.path.isdir(directory):
            console.print(f"[red]Directory not found: {directory}")
            return

        for root, _, files in os.walk(directory):
            for file in files:
                if file.endswith(".py"):
                    file_path = os.path.join(root, file)
                    self.process_file(file_path, error_message)


def main():
    parser = argparse.ArgumentParser(description="Agentic AI Debugger: Autonomously debug Python code using AI.")
    parser.add_argument("--file", type=str, help="Path to a Python file to debug.")
    parser.add_argument("--directory", type=str, help="Path to a directory containing Python files to debug.")
    parser.add_argument("--error", type=str, required=True, help="Error message or stack trace to analyze.")
    parser.add_argument("--auto-apply", action="store_true", help="Automatically apply suggested fixes.")
    parser.add_argument("--api-key", type=str, required=True, help="OpenAI API key.")

    args = parser.parse_args()

    debugger = AgenticAIDebugger(api_key=args.api_key, auto_apply=args.auto_apply)

    if args.file:
        debugger.process_file(args.file, args.error)
    elif args.directory:
        debugger.process_directory(args.directory, args.error)
    else:
        console.print("[red]You must specify either --file or --directory.")

if __name__ == "__main__":
    main()
