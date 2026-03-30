import json
import pandas as pd
import openai
import argparse

def analyze_logs(file_path, openai_api_key):
    """
    Analyze debugging logs or error trace files to identify recurring error patterns and root causes.

    Args:
        file_path (str): Path to the debugging logs file (JSON or CSV).
        openai_api_key (str): OpenAI API key for GPT-based analysis.

    Returns:
        dict: Structured insights and preventive measures.
    """
    try:
        # Load the logs file
        if file_path.endswith('.json'):
            with open(file_path, 'r') as f:
                logs = json.load(f)
        elif file_path.endswith('.csv'):
            logs = pd.read_csv(file_path).to_dict(orient='records')
        else:
            raise ValueError("Unsupported file format. Please provide a JSON or CSV file.")

        if not logs:
            return {"error": "The log file is empty or invalid."}

        # Prepare data for analysis
        log_text = "\n".join([str(log) for log in logs])

        # Use OpenAI API to analyze logs
        openai.api_key = openai_api_key
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=f"Analyze the following logs and identify recurring error patterns, root causes, and preventive measures:\n{log_text}",
            max_tokens=500
        )

        insights = response.choices[0].text.strip()

        # Return structured insights
        return {"insights": insights}

    except Exception as e:
        return {"error": str(e)}


def main():
    parser = argparse.ArgumentParser(description="Error Pattern Analyzer")
    parser.add_argument("file_path", type=str, help="Path to the debugging logs file (JSON or CSV).")
    parser.add_argument("openai_api_key", type=str, help="OpenAI API key for GPT-based analysis.")
    args = parser.parse_args()

    result = analyze_logs(args.file_path, args.openai_api_key)
    print(json.dumps(result, indent=4))


if __name__ == "__main__":
    main()