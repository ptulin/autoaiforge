import argparse
import os
import logging
from dotenv import load_dotenv
import requests
import openai

def setup_logging():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def load_env_variables():
    load_dotenv()
    return {
        "task_manager_api_key": os.getenv("TASK_MANAGER_API_KEY"),
        "claude_api_key": os.getenv("CLAUDE_API_KEY")
    }

def fetch_tasks(task_manager, api_key):
    if task_manager == "todoist":
        url = "https://api.todoist.com/rest/v1/tasks"
        headers = {"Authorization": f"Bearer {api_key}"}
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            logging.error(f"Failed to fetch tasks: {response.status_code} {response.text}")
            return []
    else:
        logging.error("Unsupported task manager")
        return []

def analyze_tasks_with_claude(tasks, api_key):
    openai.api_key = api_key
    task_descriptions = [task['content'] for task in tasks]
    prompt = (
        "You are an AI assistant. Here is a list of tasks: \n" +
        "\n".join(task_descriptions) +
        "\n\nPrioritize these tasks and suggest deadlines."
    )
    try:
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=500
        )
        return response.choices[0].text.strip()
    except openai.error.OpenAIError as e:
        logging.error(f"Error communicating with Claude AI: {e}")
        return ""

def extract_action_items_from_notes(notes, api_key):
    openai.api_key = api_key
    prompt = (
        "You are an AI assistant. Extract action items from the following meeting notes: \n" + notes
    )
    try:
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=500
        )
        return response.choices[0].text.strip()
    except openai.error.OpenAIError as e:
        logging.error(f"Error communicating with Claude AI: {e}")
        return ""

def update_task_manager_with_suggestions(task_manager, api_key, suggestions):
    if task_manager == "todoist":
        url = "https://api.todoist.com/rest/v1/tasks"
        headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
        for suggestion in suggestions.split("\n"):
            payload = {"content": suggestion}
            response = requests.post(url, headers=headers, json=payload)
            if response.status_code == 200:
                logging.info(f"Task added: {suggestion}")
            else:
                logging.error(f"Failed to add task: {response.status_code} {response.text}")
    else:
        logging.error("Unsupported task manager")

def main():
    setup_logging()

    parser = argparse.ArgumentParser(description="AI Task Syncer: Sync and prioritize tasks using Claude AI.")
    parser.add_argument("--task-manager", required=True, help="Task manager to sync with (e.g., todoist)")
    parser.add_argument("--api-key", required=False, help="API key for the task manager")
    parser.add_argument("--meeting-notes", required=False, help="Path to a text file containing meeting notes")

    args = parser.parse_args()

    env_vars = load_env_variables()
    task_manager_api_key = args.api_key or env_vars["task_manager_api_key"]
    claude_api_key = env_vars["claude_api_key"]

    if not task_manager_api_key or not claude_api_key:
        logging.error("Missing API keys. Ensure they are provided as arguments or in the .env file.")
        return

    tasks = fetch_tasks(args.task_manager, task_manager_api_key)
    if tasks:
        suggestions = analyze_tasks_with_claude(tasks, claude_api_key)
        if suggestions:
            update_task_manager_with_suggestions(args.task_manager, task_manager_api_key, suggestions)

    if args.meeting_notes:
        try:
            with open(args.meeting_notes, "r") as file:
                notes = file.read()
                action_items = extract_action_items_from_notes(notes, claude_api_key)
                if action_items:
                    update_task_manager_with_suggestions(args.task_manager, task_manager_api_key, action_items)
        except FileNotFoundError:
            logging.error(f"Meeting notes file not found: {args.meeting_notes}")

if __name__ == "__main__":
    main()