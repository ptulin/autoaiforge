import argparse
import os
from transformers import GPT2Tokenizer
import nltk
from nltk.tokenize import sent_tokenize

nltk.download('punkt')

def estimate_token_count(text, model_name="gpt2"):
    """Estimate the token count of a given text for a specific model."""
    tokenizer = GPT2Tokenizer.from_pretrained(model_name)
    tokens = tokenizer.tokenize(text)
    return len(tokens)

def summarize_text(text, max_tokens, model_name="gpt2"):
    """Summarize the text to fit within the max token limit."""
    sentences = sent_tokenize(text)
    if not sentences:
        return ""

    tokenizer = GPT2Tokenizer.from_pretrained(model_name)
    summarized = []
    current_tokens = 0

    for sentence in sentences:
        sentence_tokens = len(tokenizer.tokenize(sentence))
        if current_tokens + sentence_tokens <= max_tokens:
            summarized.append(sentence)
            current_tokens += sentence_tokens
        else:
            break

    return " ".join(summarized)

def process_input(input_data, max_tokens, model_name):
    """Process the input data and return the summarized context."""
    if os.path.isfile(input_data):
        with open(input_data, 'r', encoding='utf-8') as file:
            text = file.read()
    else:
        text = input_data

    if not text.strip():
        raise ValueError("Input text is empty.")

    return summarize_text(text, max_tokens, model_name)

def main():
    parser = argparse.ArgumentParser(description="Context Window Optimizer")
    parser.add_argument("--input", required=True, help="Path to input text file or raw text.")
    parser.add_argument("--max_tokens", type=int, required=True, help="Maximum token budget.")
    parser.add_argument("--model", default="gpt2", help="Model name for tokenization (default: gpt2).")

    args = parser.parse_args()

    try:
        summarized_context = process_input(args.input, args.max_tokens, args.model)
        print(summarized_context)
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
