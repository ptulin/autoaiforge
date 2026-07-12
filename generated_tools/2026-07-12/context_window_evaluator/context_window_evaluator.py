import argparse
import json
from pathlib import Path
from rich.console import Console
from rich.table import Table
import tiktoken
import nltk
from nltk.tokenize import word_tokenize

def analyze_prompt(prompt, tokenizer):
    """
    Analyze a single prompt for token usage, redundancy, and truncation risks.

    Args:
        prompt (str): The text of the prompt to analyze.
        tokenizer: The tokenizer instance from tiktoken.

    Returns:
        dict: Analysis results including token count, unique token count, and redundancy.
    """
    tokens = tokenizer.encode(prompt)
    token_count = len(tokens)
    unique_tokens = len(set(tokens))
    redundancy = 1 - (unique_tokens / token_count) if token_count > 0 else 0

    return {
        "token_count": token_count,
        "unique_tokens": unique_tokens,
        "redundancy": redundancy,
        "truncation_risk": token_count > tokenizer.max_token_count
    }

def analyze_file(file_path, tokenizer):
    """
    Analyze a file containing prompts.

    Args:
        file_path (str or Path): Path to the input file.
        tokenizer: The tokenizer instance from tiktoken.

    Returns:
        list: A list of analysis results for each prompt.
    """
    results = []
    try:
        file_path = Path(file_path)  # Ensure file_path is a Path object
        with open(file_path, 'r', encoding='utf-8') as file:
            if file_path.suffix == '.json':
                data = json.load(file)
                prompts = data if isinstance(data, list) else [data]
            else:
                prompts = file.readlines()

            for prompt in prompts:
                prompt = prompt.strip()
                if prompt:
                    results.append(analyze_prompt(prompt, tokenizer))
    except Exception as e:
        raise ValueError(f"Error processing file {file_path}: {e}")

    return results

def generate_report(analysis_results, output_file=None):
    """
    Generate a report from the analysis results.

    Args:
        analysis_results (list): List of analysis results.
        output_file (str, optional): Path to save the report as JSON.

    Returns:
        None
    """
    console = Console()
    table = Table(title="Context Window Analysis Report")

    table.add_column("Prompt #", justify="right", style="cyan")
    table.add_column("Token Count", justify="right", style="green")
    table.add_column("Unique Tokens", justify="right", style="magenta")
    table.add_column("Redundancy", justify="right", style="yellow")
    table.add_column("Truncation Risk", justify="right", style="red")

    for idx, result in enumerate(analysis_results, start=1):
        table.add_row(
            str(idx),
            str(result["token_count"]),
            str(result["unique_tokens"]),
            f"{result['redundancy']:.2f}",
            "Yes" if result["truncation_risk"] else "No"
        )

    console.print(table)

    if output_file:
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(analysis_results, f, indent=4)

def main():
    parser = argparse.ArgumentParser(description="Context Window Evaluator")
    parser.add_argument('--input', required=True, nargs='+', help="Input text or JSON file(s) containing prompts.")
    parser.add_argument('--output', help="Optional output file to save the analysis report in JSON format.")
    args = parser.parse_args()

    nltk.download('punkt', quiet=True)
    tokenizer = tiktoken.get_encoding("cl100k_base")
    tokenizer.max_token_count = 4096

    all_results = []

    for input_file in args.input:
        file_path = Path(input_file)
        if not file_path.exists():
            print(f"Error: File not found - {file_path}")
            continue

        try:
            results = analyze_file(file_path, tokenizer)
            all_results.extend(results)
        except ValueError as e:
            print(e)

    generate_report(all_results, args.output)

if __name__ == "__main__":
    main()