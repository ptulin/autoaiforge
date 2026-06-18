import argparse
import nltk
from transformers import pipeline
from Levenshtein import ratio

# Download necessary NLTK data
nltk.download('punkt')

def compress_prompt(prompt: str, verbosity: int = 1) -> str:
    """
    Compresses a given prompt by removing redundancy and simplifying language.

    Args:
        prompt (str): The input prompt to compress.
        verbosity (int): Level of verbosity for compression (1: high, 2: medium, 3: low).

    Returns:
        str: The compressed prompt.
    """
    if not prompt.strip():
        return ""

    # Tokenize sentences
    sentences = nltk.sent_tokenize(prompt)

    # Use a summarization pipeline from transformers
    summarizer = pipeline("summarization")

    compressed_sentences = []
    for sentence in sentences:
        try:
            summary = summarizer(sentence, max_length=15 * verbosity, min_length=5 * verbosity, do_sample=False)
            compressed_sentences.append(summary[0]['summary_text'])
        except Exception:
            compressed_sentences.append(sentence)  # Fallback to original sentence if summarization fails

    compressed_prompt = " ".join(compressed_sentences)

    # Remove redundancy by comparing sentence similarity
    unique_sentences = []
    for sentence in compressed_sentences:
        if not any(ratio(sentence, s) > 0.8 for s in unique_sentences):
            unique_sentences.append(sentence)

    return " ".join(unique_sentences)

def main():
    parser = argparse.ArgumentParser(description="Prompt Compressor: Compress prompts while retaining semantic meaning.")
    parser.add_argument("prompt", type=str, help="The input prompt to compress.")
    parser.add_argument("--verbosity", type=int, default=1, choices=[1, 2, 3], help="Verbosity level for compression (1: high, 2: medium, 3: low). Default is 1.")

    args = parser.parse_args()

    compressed = compress_prompt(args.prompt, args.verbosity)
    print(compressed)

if __name__ == "__main__":
    main()