import argparse
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import nltk
from nltk.tokenize import word_tokenize, sent_tokenize
from collections import Counter
import math

def calculate_entropy(text):
    """Calculate the entropy of a given text."""
    words = word_tokenize(text)
    total_words = len(words)
    word_freq = Counter(words)
    entropy = -sum((freq / total_words) * math.log2(freq / total_words) for freq in word_freq.values())
    return entropy

def extract_features(text):
    """Extract linguistic features from the given text."""
    if not text.strip():
        raise ValueError("Input text cannot be empty")

    sentences = sent_tokenize(text)
    words = word_tokenize(text)

    num_sentences = len(sentences)
    num_words = len(words)
    avg_sentence_length = num_words / num_sentences if num_sentences > 0 else 0
    word_freq = Counter(words)
    entropy = calculate_entropy(text)

    features = {
        "num_sentences": num_sentences,
        "num_words": num_words,
        "avg_sentence_length": avg_sentence_length,
        "entropy": entropy,
        "word_frequency": word_freq,
        "text": text  # Include the original text for visualization purposes
    }

    return features

def visualize_features(features, output_file=None):
    """Visualize extracted features using histograms and scatter plots."""
    if not features:
        raise ValueError("Features cannot be empty")

    # Word frequency distribution
    word_freq_df = pd.DataFrame(features["word_frequency"].items(), columns=["Word", "Frequency"])
    word_freq_df = word_freq_df.sort_values(by="Frequency", ascending=False)

    plt.figure(figsize=(10, 6))
    sns.barplot(x="Frequency", y="Word", data=word_freq_df.head(20), palette="viridis")
    plt.title("Top 20 Word Frequencies")
    plt.xlabel("Frequency")
    plt.ylabel("Word")
    if output_file:
        plt.savefig(output_file + "_word_freq.png")
    else:
        plt.show()

    # Sentence length distribution
    sentence_lengths = [len(word_tokenize(sentence)) for sentence in sent_tokenize(features['text'])]

    plt.figure(figsize=(10, 6))
    sns.histplot(sentence_lengths, bins=20, kde=True, color="blue")
    plt.title("Sentence Length Distribution")
    plt.xlabel("Sentence Length")
    plt.ylabel("Frequency")
    if output_file:
        plt.savefig(output_file + "_sentence_length.png")
    else:
        plt.show()

def main():
    parser = argparse.ArgumentParser(description="Feature Inspector for LLM Detection")
    parser.add_argument("input", help="Input text file or string")
    parser.add_argument("--output", help="Output file prefix for visualizations", default=None)
    args = parser.parse_args()

    # Read input
    try:
        with open(args.input, "r") as f:
            text = f.read()
    except FileNotFoundError:
        text = args.input

    # Extract features
    features = extract_features(text)

    # Visualize features
    visualize_features(features, output_file=args.output)

if __name__ == "__main__":
    nltk.download('punkt', quiet=True)
    main()
