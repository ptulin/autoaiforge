import argparse
import json
import csv
import os
from datetime import datetime
import pandas as pd
from openai import ChatCompletion

class ClaudeConversationLogger:
    def __init__(self, api_key):
        self.api_key = api_key
        self.logs = []

    def log_interaction(self, prompt, response, tags):
        timestamp = datetime.now().isoformat()
        self.logs.append({
            "timestamp": timestamp,
            "prompt": prompt,
            "response": response,
            "tags": tags
        })

    def export_logs(self, file_path, file_format):
        if file_format == "csv":
            df = pd.DataFrame(self.logs)
            df.to_csv(file_path, index=False)
        elif file_format == "json":
            with open(file_path, "w") as f:
                json.dump(self.logs, f, indent=4)
        else:
            raise ValueError("Unsupported file format. Use 'csv' or 'json'.")

    def interact_with_claude(self, prompt):
        try:
            response = ChatCompletion.create(
                model="claude-v1",
                messages=[{"role": "user", "content": prompt}]
            )
            return response.choices[0].message["content"]
        except Exception as e:
            raise RuntimeError(f"Error interacting with Claude: {e}")

def main():
    parser = argparse.ArgumentParser(description="Claude Conversation Logger")
    parser.add_argument("--prompt", required=True, help="Prompt to send to Claude")
    parser.add_argument("--tag", required=True, help="Tag or category for the interaction")
    parser.add_argument("--export", required=True, help="File path to export logs (CSV or JSON)")
    parser.add_argument("--format", choices=["csv", "json"], required=True, help="Export file format")
    parser.add_argument("--api_key", required=True, help="OpenAI API key")

    args = parser.parse_args()

    logger = ClaudeConversationLogger(api_key=args.api_key)

    try:
        response = logger.interact_with_claude(args.prompt)
        logger.log_interaction(args.prompt, response, args.tag)
        logger.export_logs(args.export, args.format)
        print(f"Logs successfully exported to {args.export}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()