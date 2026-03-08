import argparse
import pandas as pd
import matplotlib.pyplot as plt
import openai
import os

def analyze_dataset(file_path, query, api_key):
    """
    Analyzes a dataset using GPT-5.4 to provide insights based on a natural language query.

    Args:
        file_path (str): Path to the dataset file (CSV or Excel).
        query (str): Natural language query for analysis.
        api_key (str): OpenAI API key.

    Returns:
        str: Analysis result from GPT-5.4.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"The file {file_path} does not exist.")

    # Load dataset
    try:
        if file_path.endswith('.csv'):
            df = pd.read_csv(file_path)
        elif file_path.endswith(('.xls', '.xlsx')):
            df = pd.read_excel(file_path)
        else:
            raise ValueError("Unsupported file format. Please provide a CSV or Excel file.")
    except Exception as e:
        raise ValueError(f"Error loading dataset: {e}")

    if df.empty:
        return "The dataset is empty."

    # Prepare dataset summary for GPT
    dataset_preview = df.head(10).to_csv(index=False)
    columns = ", ".join(df.columns)
    dataset_info = f"The dataset has {len(df)} rows and {len(df.columns)} columns. The columns are: {columns}."

    # GPT prompt
    prompt = (
        f"You are a data analyst. Here is a preview of the dataset:\n\n"
        f"{dataset_preview}\n\n"
        f"{dataset_info}\n\n"
        f"Based on the following query, provide an analysis:\n\n"
        f"{query}"
    )

    # Call GPT-5.4
    openai.api_key = api_key
    try:
        response = openai.Completion.create(
            engine="gpt-4",  # Assuming GPT-5.4 is backward compatible with GPT-4 API
            prompt=prompt,
            max_tokens=1000,
            temperature=0.7
        )
        return response.choices[0].text.strip()
    except Exception as e:
        raise ConnectionError(f"Error communicating with OpenAI API: {e}")

def main():
    parser = argparse.ArgumentParser(description="Dataset Explorer for GPT-5.4")
    parser.add_argument('--input', required=True, help="Path to the input CSV/Excel file.")
    parser.add_argument('--query', required=True, help="Natural language query for dataset analysis.")
    parser.add_argument('--api_key', required=True, help="OpenAI API key.")
    parser.add_argument('--output', help="Path to save the analysis report.")

    args = parser.parse_args()

    try:
        result = analyze_dataset(args.input, args.query, args.api_key)
        print("\nAnalysis Result:\n")
        print(result)

        if args.output:
            with open(args.output, 'w') as f:
                f.write(result)
            print(f"\nAnalysis saved to {args.output}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()