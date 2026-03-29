import json
import argparse
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

def create_slack_workflow(slack_token, trigger_channel, prompt):
    """
    Creates a Slack workflow that triggers Claude AI to process messages in a given channel.

    Args:
        slack_token (str): Slack API token.
        trigger_channel (str): Slack channel to monitor for triggers.
        prompt (str): Prompt logic for Claude AI.

    Returns:
        dict: Workflow creation result.
    """
    slack_client = WebClient(token=slack_token)

    try:
        # Fetch channel ID from channel name
        response = slack_client.conversations_list()
        channels = response.get("channels", [])
        channel_id = None
        for channel in channels:
            if channel.get("name") == trigger_channel.lstrip("#"):
                channel_id = channel.get("id")
                break

        if not channel_id:
            raise ValueError(f"Channel '{trigger_channel}' not found.")

        # Simulate workflow creation (Slack doesn't have a direct API for workflows)
        workflow = {
            "name": "Claude Workflow",
            "trigger_channel": trigger_channel,
            "prompt": prompt
        }

        # Log the workflow creation (mocking actual Slack workflow creation)
        print("Workflow created:", json.dumps(workflow, indent=2))

        return workflow

    except SlackApiError as e:
        raise RuntimeError(f"Slack API error: {e.response['error']}")
    except Exception as e:
        raise RuntimeError(f"Error creating workflow: {str(e)}")

def main():
    parser = argparse.ArgumentParser(description="Claude Slack Workflow Bot")
    parser.add_argument("--slack-token", required=True, help="Your Slack API token.")
    parser.add_argument("--trigger", required=True, help="The Slack channel to monitor (e.g., #general).")
    parser.add_argument("--prompt", required=True, help="The prompt logic for Claude AI.")

    args = parser.parse_args()

    try:
        workflow = create_slack_workflow(args.slack_token, args.trigger, args.prompt)
        print("Workflow successfully created:")
        print(json.dumps(workflow, indent=2))
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()