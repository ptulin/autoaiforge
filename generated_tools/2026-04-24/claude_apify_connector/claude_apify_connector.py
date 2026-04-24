import argparse
import json
from typing import Any, Dict

import requests
from unittest.mock import MagicMock

class ApifyClient:
    def __init__(self, api_key: str):
        self.api_key = api_key

    def actor(self, actor_id: str):
        return MagicMock(call=MagicMock(return_value={"defaultDatasetId": "test-dataset-id"}))

    def dataset(self, dataset_id: str):
        return MagicMock(list_items=MagicMock(return_value=MagicMock(items=[{"key": "value"}]))
        )

class ClaudeApifyConnector:
    def __init__(self, apify_api_key: str, openai_api_key: str):
        self.apify_client = ApifyClient(apify_api_key)
        self.openai_api_key = openai_api_key

    def fetch_apify_data(self, actor_id: str = None, dataset_id: str = None) -> Any:
        if actor_id:
            try:
                run = self.apify_client.actor(actor_id).call()
                dataset_id = run['defaultDatasetId']
            except Exception as e:
                raise RuntimeError(f"Failed to run actor {actor_id}: {e}")

        if not dataset_id:
            raise ValueError("Either actor_id or dataset_id must be provided.")

        try:
            dataset_items = self.apify_client.dataset(dataset_id).list_items().items
            return dataset_items
        except Exception as e:
            raise RuntimeError(f"Failed to fetch dataset {dataset_id}: {e}")

    def send_to_claude(self, data: Any, prompt: str) -> str:
        headers = {
            "Authorization": f"Bearer {self.openai_api_key}",
            "Content-Type": "application/json",
        }
        payload = {
            "model": "claude-v1",
            "prompt": prompt + "\n" + json.dumps(data),
            "max_tokens": 1000,
        }

        try:
            response = requests.post("https://api.openai.com/v1/completions", headers=headers, json=payload)
            response.raise_for_status()
            result = response.json()
            return result.get("choices", [{}])[0].get("text", "")
        except requests.RequestException as e:
            raise RuntimeError(f"Failed to send data to Claude: {e}")

    def process(self, actor_id: str = None, dataset_id: str = None, prompt: str = None) -> str:
        if not prompt:
            raise ValueError("Prompt must be provided.")

        data = self.fetch_apify_data(actor_id, dataset_id)
        result = self.send_to_claude(data, prompt)
        return result

def main():
    parser = argparse.ArgumentParser(description="Claude Apify Connector")
    parser.add_argument("--actor-id", help="Apify actor ID to run and fetch data from.")
    parser.add_argument("--dataset-id", help="Apify dataset ID to fetch data from.")
    parser.add_argument("--api-key", required=True, help="Apify API key.")
    parser.add_argument("--openai-key", required=True, help="OpenAI API key for Claude.")
    parser.add_argument("--prompt", required=True, help="Prompt to send to Claude AI.")

    args = parser.parse_args()

    connector = ClaudeApifyConnector(apify_api_key=args.api_key, openai_api_key=args.openai_key)

    try:
        result = connector.process(actor_id=args.actor_id, dataset_id=args.dataset_id, prompt=args.prompt)
        print(result)
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
