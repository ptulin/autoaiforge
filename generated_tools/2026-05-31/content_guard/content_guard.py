import json
import sys
import argparse
from transformers import pipeline

def classify_text(text, classifier):
    """
    Classifies the given text using the provided classifier.

    Args:
        text (str): The input text to classify.
        classifier: The NLP pipeline for text classification.

    Returns:
        list: A list of flagged results with labels and scores.
    """
    results = classifier(text)
    flagged = [result for result in results if result['score'] > 0.5]
    return flagged

def main():
    """
    Main function for the Content Guard CLI tool.

    Parses command-line arguments and processes the input file.
    """
    parser = argparse.ArgumentParser(description="Content Guard: Detect harmful or inappropriate text.")
    parser.add_argument('--input', '-i', type=str, required=True, help='Path to the input text file.')
    parser.add_argument('--output', '-o', type=str, help='Path to save the flagged content as JSON.')
    args = parser.parse_args()

    # Initialize the text classification pipeline
    try:
        classifier = pipeline('text-classification', model='unitary/toxic-bert')
    except Exception as e:
        print(f"Error initializing classifier: {e}", file=sys.stderr)
        sys.exit(1)

    # Read input text
    try:
        with open(args.input, 'r') as file:
            text = file.read()
    except FileNotFoundError:
        print("Error: Input file not found.", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error reading input file: {e}", file=sys.stderr)
        sys.exit(1)

    # Classify text
    flagged = classify_text(text, classifier)

    # Output results
    if args.output:
        try:
            with open(args.output, 'w') as file:
                json.dump(flagged, file, indent=4)
            print(f"Flagged content saved to {args.output}")
        except Exception as e:
            print(f"Error writing to output file: {e}", file=sys.stderr)
            sys.exit(1)
    else:
        print(json.dumps(flagged, indent=4))

if __name__ == "__main__":
    main()
