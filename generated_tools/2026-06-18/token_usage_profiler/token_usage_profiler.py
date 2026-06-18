import argparse
import os
from tabulate import tabulate
import tiktoken

def analyze_prompt(file_path):
    """
    Analyze token usage in the given prompt file.

    Args:
        file_path (str): Path to the prompt text file.

    Returns:
        dict: Analysis report containing token counts, high-frequency tokens, and optimization suggestions.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    if not content.strip():
        raise ValueError("The input file is empty.")

    encoder = tiktoken.get_encoding("cl100k_base")
    tokens = encoder.encode(content)

    token_count = len(tokens)

    # Token frequency analysis
    token_frequency = {}
    for token in tokens:
        token_frequency[token] = token_frequency.get(token, 0) + 1

    sorted_tokens = sorted(token_frequency.items(), key=lambda x: x[1], reverse=True)

    # Optimization suggestions
    suggestions = []
    if token_count > 1000:
        suggestions.append("Consider reducing the length of the prompt to decrease token usage.")
    if sorted_tokens and sorted_tokens[0][1] > token_count * 0.1:
        suggestions.append("High-frequency tokens detected. Consider rephrasing to reduce repetition.")

    return {
        "total_tokens": token_count,
        "high_frequency_tokens": sorted_tokens[:10],
        "suggestions": suggestions
    }

def generate_report(analysis):
    """
    Generate a tabular report from the analysis.

    Args:
        analysis (dict): Analysis report.

    Returns:
        str: Tabular report as a string.
    """
    report = []
    report.append(["Total Tokens", analysis["total_tokens"]])

    if analysis["high_frequency_tokens"]:
        report.append(["High-Frequency Tokens", ""])
        for token, count in analysis["high_frequency_tokens"]:
            report.append([f"Token ID {token}", count])

    if analysis["suggestions"]:
        report.append(["Optimization Suggestions", ""])
        for suggestion in analysis["suggestions"]:
            report.append(["-", suggestion])

    return tabulate(report, headers=["Metric", "Value"], tablefmt="grid")

def main():
    parser = argparse.ArgumentParser(description="Token Usage Profiler: Analyze token usage in prompts.")
    parser.add_argument("--input", required=True, help="Path to the input prompt text file.")

    args = parser.parse_args()

    try:
        analysis = analyze_prompt(args.input)
        report = generate_report(analysis)
        print(report)
    except FileNotFoundError as e:
        print(f"Error: {e}")
    except ValueError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()
