import argparse
import pandas as pd
from dateutil import parser as date_parser
import openai
import os

def summarize_updates(updates_file, openai_api_key):
    try:
        # Load the updates file
        if updates_file.endswith('.csv'):
            updates = pd.read_csv(updates_file)
        elif updates_file.endswith('.json'):
            updates = pd.read_json(updates_file, convert_dates=False)
        else:
            raise ValueError("Unsupported file format. Please provide a CSV or JSON file.")

        # Validate required columns
        required_columns = {'task_id', 'developer', 'status', 'description', 'updated_at'}
        if not required_columns.issubset(updates.columns):
            raise ValueError(f"Input file must contain the following columns: {', '.join(required_columns)}")

        # Parse dates
        updates['updated_at'] = updates['updated_at'].apply(lambda x: date_parser.parse(str(x)))

        # Prepare data for OpenAI summarization
        updates_summary = updates.groupby('developer').apply(
            lambda group: {
                'developer': group.name,
                'tasks': group[['task_id', 'status', 'description']].to_dict(orient='records')
            }
        ).tolist()

        # Generate Scrum agenda and summaries using OpenAI
        openai.api_key = openai_api_key
        prompt = (
            "You are a Scrum Master AI. Based on the following task updates, generate a Scrum meeting agenda, "
            "highlighting progress, blockers, and a summary for each developer:\n\n"
            f"{updates_summary}\n\n"
            "Provide the agenda and summaries in a clear and concise format."
        )

        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=500
        )

        return response['choices'][0]['text'].strip()

    except Exception as e:
        return f"Error: {str(e)}"


def main():
    parser = argparse.ArgumentParser(description="Daily Scrum AI Assistant")
    parser.add_argument('--updates_file', required=True, help="Path to the project updates file (CSV or JSON).")
    parser.add_argument('--openai_api_key', required=True, help="OpenAI API key for generating summaries.")
    args = parser.parse_args()

    result = summarize_updates(args.updates_file, args.openai_api_key)
    print(result)


if __name__ == "__main__":
    main()