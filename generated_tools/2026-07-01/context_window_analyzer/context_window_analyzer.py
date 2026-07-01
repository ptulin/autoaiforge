import argparse
import json
import os
import matplotlib.pyplot as plt
from unittest.mock import MagicMock

# Mocking tiktoken for testing purposes
def mock_get_encoding(encoding_name):
    class MockTokenizer:
        def encode(self, text):
            return text.split()  # Simple tokenization by splitting on spaces

    return MockTokenizer()

try:
    import tiktoken
except ImportError:
    tiktoken = MagicMock()
    tiktoken.get_encoding = mock_get_encoding

def analyze_tokens(input_data, tokenizer):
    """Analyze token usage in the input data."""
    token_counts = []
    inefficiencies = []

    for idx, section in enumerate(input_data):
        tokens = tokenizer.encode(section)
        token_counts.append(len(tokens))

        if len(tokens) > 100:  # Example inefficiency threshold
            inefficiencies.append((idx, len(tokens), section[:50]))

    return token_counts, inefficiencies

def visualize_token_distribution(token_counts):
    """Visualize token distribution as a histogram."""
    plt.hist(token_counts, bins=10, color='skyblue', edgecolor='black')
    plt.title('Token Distribution')
    plt.xlabel('Number of Tokens')
    plt.ylabel('Frequency')
    plt.grid(True)
    plt.show()

def process_input_file(file_path):
    """Process the input file and return the data as a list of strings."""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    with open(file_path, 'r', encoding='utf-8') as file:
        if file_path.endswith('.json'):
            data = json.load(file)
            if not isinstance(data, list):
                raise ValueError("JSON file must contain a list of strings.")
        else:
            data = file.read().splitlines()

    return data

def main():
    parser = argparse.ArgumentParser(description="Context Window Analyzer")
    parser.add_argument('--input', required=True, help="Path to input text or JSON file.")
    parser.add_argument('--visualize', action='store_true', help="Display token distribution visualization.")
    args = parser.parse_args()

    try:
        input_data = process_input_file(args.input)
        tokenizer = tiktoken.get_encoding("cl100k_base")

        token_counts, inefficiencies = analyze_tokens(input_data, tokenizer)

        print("Token Analysis Summary:")
        print(f"Total Sections: {len(input_data)}")
        print(f"Total Tokens: {sum(token_counts)}")
        print("Inefficient Sections:")
        for idx, count, snippet in inefficiencies:
            print(f"  Section {idx + 1}: {count} tokens, starts with: {snippet}...")

        if args.visualize:
            visualize_token_distribution(token_counts)

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()