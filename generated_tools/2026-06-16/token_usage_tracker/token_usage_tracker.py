import os
import json
import requests
import click
from tabulate import tabulate

class TokenUsageTracker:
    def __init__(self, api_key, model):
        self.api_key = api_key
        self.model = model
        self.usage_log = []

    def make_request(self, prompt):
        """Simulates an API call to an AI model and tracks token usage."""
        headers = {"Authorization": f"Bearer {self.api_key}"}
        payload = {"model": self.model, "prompt": prompt}

        try:
            response = requests.post("https://api.openai.com/v1/completions", headers=headers, json=payload)
            response.raise_for_status()
            data = response.json()

            # Simulate token usage tracking
            tokens_used = data.get("usage", {}).get("total_tokens", 0)
            self.usage_log.append({"prompt": prompt, "tokens_used": tokens_used})
            return data

        except requests.exceptions.RequestException as e:
            click.echo(f"Error: {e}")
            return None

    def generate_report(self, output_format="text"):
        """Generates a summary report of token usage."""
        if not self.usage_log:
            return "No usage data to report."

        total_tokens = sum(entry["tokens_used"] for entry in self.usage_log)
        report_data = [
            [i + 1, entry["prompt"], entry["tokens_used"]] for i, entry in enumerate(self.usage_log)
        ]
        report_data.append(["Total", "", total_tokens])

        if output_format == "text":
            return tabulate(report_data, headers=["#", "Prompt", "Tokens Used"], tablefmt="grid")
        elif output_format == "csv":
            csv_data = "#;Prompt;Tokens Used\n"
            csv_data += "\n".join(f"{row[0]};{row[1]};{row[2]}" for row in report_data)
            return csv_data
        else:
            return "Invalid output format."

@click.command()
@click.option("--api_key", required=True, help="Your API key for the AI service.")
@click.option("--model", required=True, help="The model to use (e.g., gpt-4).")
@click.option("--output_format", default="text", type=click.Choice(["text", "csv"]), help="Output format for the report.")
def main(api_key, model, output_format):
    """Token Usage Tracker: Monitors token usage for AI model API calls."""
    tracker = TokenUsageTracker(api_key, model)

    click.echo("Enter prompts (type 'exit' to finish):")
    while True:
        prompt = input("Prompt: ")
        if prompt.lower() == "exit":
            break
        tracker.make_request(prompt)

    report = tracker.generate_report(output_format)
    click.echo(report)

if __name__ == "__main__":
    main()