import os
import argparse
from tqdm import tqdm
import openai

def summarize_text(api_key, text, max_tokens=100):
    """Summarize the given text using OpenAI's API."""
    openai.api_key = api_key
    try:
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=f"Summarize the following text:\n{text}\n", 
            max_tokens=max_tokens
        )
        return response["choices"][0]["text"].strip()
    except Exception as e:
        raise RuntimeError(f"Error during summarization: {e}")

def process_files(input_dir, output_dir, api_key, max_tokens):
    """Process all text files in the input directory and save summaries."""
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for filename in tqdm(os.listdir(input_dir), desc="Processing files"):
        input_path = os.path.join(input_dir, filename)
        if os.path.isfile(input_path) and filename.endswith(".txt"):
            with open(input_path, "r", encoding="utf-8") as file:
                text = file.read()

            if not text.strip():
                print(f"Skipping empty file: {filename}")
                continue

            try:
                summary = summarize_text(api_key, text, max_tokens)
                output_path = os.path.join(output_dir, f"summary_{filename}")
                with open(output_path, "w", encoding="utf-8") as summary_file:
                    summary_file.write(summary)
            except RuntimeError as e:
                print(f"Failed to summarize {filename}: {e}")

def main():
    parser = argparse.ArgumentParser(description="Batch Text Summarizer")
    parser.add_argument("--input-dir", required=True, help="Path to the directory containing text files")
    parser.add_argument("--output-dir", required=True, help="Path to the directory where summaries will be saved")
    parser.add_argument("--api-key", required=True, help="OpenAI API key for text summarization")
    parser.add_argument("--max-tokens", type=int, default=100, help="Maximum number of tokens for the summary")

    args = parser.parse_args()

    try:
        process_files(args.input_dir, args.output_dir, args.api_key, args.max_tokens)
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()