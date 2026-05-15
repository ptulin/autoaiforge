import argparse
import requests
import pandas as pd
from tqdm import tqdm
import json

def process_data(input_file, skill, output_file):
    """
    Process data using Claude AI Skills.

    Args:
        input_file (str): Path to the input file (CSV, JSON, or TXT).
        skill (str): Claude AI skill to apply (e.g., 'summarize').
        output_file (str): Path to the output file.

    Returns:
        None
    """
    # Determine file format
    file_extension = input_file.split('.')[-1].lower()
    if file_extension not in ['csv', 'json', 'txt']:
        raise ValueError("Unsupported file format. Supported formats: CSV, JSON, TXT.")

    # Read input data
    if file_extension == 'csv':
        data = pd.read_csv(input_file)
    elif file_extension == 'json':
        with open(input_file, 'r') as f:
            data = json.load(f)
    else:  # TXT
        with open(input_file, 'r') as f:
            data = f.readlines()

    # Prepare data for processing
    if isinstance(data, pd.DataFrame):
        records = data.to_dict(orient='records')
    elif isinstance(data, list):
        if isinstance(data[0], dict):
            records = data  # JSON list of dicts
        else:
            records = [{'text': line.strip()} for line in data]  # TXT list of strings
    else:
        raise ValueError("Invalid data format.")

    processed_records = []

    # Process data with Claude API
    for record in tqdm(records, desc="Processing records"):
        try:
            response = requests.post(
                "https://api.claude.ai/skills",
                json={"skill": skill, "data": record},
                timeout=10
            )
            response.raise_for_status()
            processed_records.append(response.json())
        except requests.exceptions.RequestException as e:
            processed_records.append({"error": str(e), "data": record})

    # Save output data
    if file_extension == 'csv':
        pd.DataFrame(processed_records).to_csv(output_file, index=False)
    elif file_extension == 'json':
        with open(output_file, 'w') as f:
            json.dump(processed_records, f, indent=4)
    else:  # TXT
        with open(output_file, 'w') as f:
            for record in processed_records:
                f.write(json.dumps(record) + '\n')

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Claude Batch Automator")
    parser.add_argument('--input', required=True, help="Path to the input file (CSV, JSON, or TXT).")
    parser.add_argument('--skill', required=True, help="Claude AI skill to apply (e.g., 'summarize').")
    parser.add_argument('--output', required=True, help="Path to the output file.")

    args = parser.parse_args()

    try:
        process_data(args.input, args.skill, args.output)
        print(f"Processing completed. Output saved to {args.output}")
    except Exception as e:
        print(f"Error: {e}")