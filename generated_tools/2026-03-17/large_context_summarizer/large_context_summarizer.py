import argparse
import json
import os
from typing import List, Union
import openai
import tiktoken

def recursive_summarize(text: str, depth: int, granularity: int) -> str:
    """
    Recursively summarize the given text to the specified depth and granularity.

    Args:
        text (str): The input text to summarize.
        depth (int): The number of recursive summarization levels.
        granularity (int): The number of chunks to divide the text into at each level.

    Returns:
        str: The summarized text.
    """
    if depth <= 0 or len(text.strip()) == 0:
        return text

    encoding = tiktoken.encoding_for_model("gpt-3.5-turbo")
    tokens = encoding.encode(text)
    chunk_size = max(1, len(tokens) // granularity)

    chunks = [
        encoding.decode(tokens[i:i + chunk_size])
        for i in range(0, len(tokens), chunk_size)
    ]

    summaries = []
    for chunk in chunks:
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": f"Summarize this: {chunk}"}]
            )
            summaries.append(response["choices"][0]["message"]["content"].strip())
        except Exception as e:
            summaries.append(f"[Error summarizing chunk: {str(e)}]")

    return recursive_summarize(" ".join(summaries), depth - 1, granularity)

def load_input_file(file_path: str) -> str:
    """Load text data from a file."""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Input file '{file_path}' does not exist.")

    with open(file_path, "r", encoding="utf-8") as file:
        if file_path.endswith(".json"):
            data = json.load(file)
            return json.dumps(data) if isinstance(data, (dict, list)) else str(data)
        elif file_path.endswith(".txt"):
            return file.read()
        else:
            raise ValueError("Unsupported file format. Only .txt and .json are allowed.")

def save_output_file(output: Union[str, dict], output_path: str):
    """Save the summarized output to a file."""
    with open(output_path, "w", encoding="utf-8") as file:
        if output_path.endswith(".json"):
            json.dump(output, file, indent=4)
        elif output_path.endswith(".txt"):
            file.write(output)
        else:
            raise ValueError("Unsupported file format. Only .txt and .json are allowed.")

def main():
    parser = argparse.ArgumentParser(description="Large Context Summarizer")
    parser.add_argument("--input", required=True, help="Path to the input text or JSON file.")
    parser.add_argument("--depth", type=int, default=3, help="Depth of recursive summarization.")
    parser.add_argument("--granularity", type=int, default=5, help="Number of chunks per summarization level.")
    parser.add_argument("--output", help="Path to save the summarized output (optional).")

    args = parser.parse_args()

    try:
        input_text = load_input_file(args.input)
        summarized_text = recursive_summarize(input_text, args.depth, args.granularity)

        if args.output:
            save_output_file(summarized_text, args.output)
        else:
            print(summarized_text)
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()