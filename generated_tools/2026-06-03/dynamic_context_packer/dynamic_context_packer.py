import json
import argparse
import pandas as pd
import tiktoken

def load_data(input_files):
    """Load data from JSON files."""
    data = []
    for file in input_files:
        try:
            with open(file, 'r') as f:
                data.append(json.load(f))
        except FileNotFoundError:
            raise FileNotFoundError(f"File not found: {file}")
        except json.JSONDecodeError:
            raise ValueError(f"Invalid JSON format in file: {file}")
    return data

def calculate_tokens(text, encoding_name='cl100k_base'):
    """Calculate the number of tokens in a given text using tiktoken."""
    encoding = tiktoken.get_encoding(encoding_name)
    return len(encoding.encode(text))

def pack_context(data, max_tokens, rules):
    """Pack mixed data types into a single context window."""
    packed_context = ""
    for item in data:
        if isinstance(item, dict):
            for key, value in item.items():
                entry = f"{key}: {value}\n"
                if calculate_tokens(packed_context + entry) <= max_tokens:
                    packed_context += entry
                else:
                    break
        elif isinstance(item, list):
            for sub_item in item:
                entry = f"- {sub_item}\n"
                if calculate_tokens(packed_context + entry) <= max_tokens:
                    packed_context += entry
                else:
                    break
        else:
            entry = f"{item}\n"
            if calculate_tokens(packed_context + entry) <= max_tokens:
                packed_context += entry
            else:
                break
    return packed_context

def save_output(output, output_file):
    """Save the packed context to a file."""
    try:
        with open(output_file, 'w') as f:
            f.write(output)
    except Exception as e:
        raise IOError(f"Failed to save output to {output_file}: {e}")

def main():
    parser = argparse.ArgumentParser(description="Dynamic Context Packer")
    parser.add_argument('--input', nargs='+', required=True, help="Input JSON file(s)")
    parser.add_argument('--max_tokens', type=int, required=True, help="Maximum token limit")
    parser.add_argument('--output', required=True, help="Output file")
    parser.add_argument('--rules', type=str, default='', help="Packing rules (optional)")

    args = parser.parse_args()

    try:
        data = load_data(args.input)
        packed_context = pack_context(data, args.max_tokens, args.rules)
        save_output(packed_context, args.output)
        print(f"Context packed successfully into {args.output}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()