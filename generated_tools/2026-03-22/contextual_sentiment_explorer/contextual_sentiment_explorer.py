import argparse
import sys
from transformers import pipeline
from nltk.tokenize import sent_tokenize
from rich.console import Console
from rich.table import Table
import nltk

def analyze_sentiment(text):
    """Analyze sentiment of the given text and highlight key phrases."""
    nltk.download('punkt', quiet=True)  # Ensure the tokenizer data is downloaded
    sentiment_analyzer = pipeline("sentiment-analysis")
    sentences = sent_tokenize(text)
    results = []

    for sentence in sentences:
        result = sentiment_analyzer(sentence)[0]
        results.append({
            "sentence": sentence,
            "label": result['label'],
            "score": result['score']
        })

    return results

def display_results(results):
    """Display sentiment analysis results in a table format."""
    console = Console()
    table = Table(title="Contextual Sentiment Analysis")

    table.add_column("Sentence", style="dim", overflow="fold")
    table.add_column("Sentiment", justify="center")
    table.add_column("Score", justify="center")

    for result in results:
        table.add_row(result['sentence'], result['label'], f"{result['score']:.2f}")

    console.print(table)

def main():
    parser = argparse.ArgumentParser(description="Contextual Sentiment Explorer")
    parser.add_argument("--input", type=str, help="Path to input text file")
    args = parser.parse_args()

    if args.input:
        try:
            with open(args.input, "r", encoding="utf-8") as file:
                text = file.read()
        except FileNotFoundError:
            print("Error: File not found.")
            sys.exit(1)
    else:
        print("Reading from stdin. Press Ctrl+D to submit.")
        text = sys.stdin.read()

    if not text.strip():
        print("Error: No input text provided.")
        sys.exit(1)

    results = analyze_sentiment(text)
    display_results(results)

if __name__ == "__main__":
    main()
