import argparse
import json
import os
import re
from collections import Counter
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import spacy
from nltk.sentiment import SentimentIntensityAnalyzer
from nltk import download

def load_input(input_path):
    """Load input from a file."""
    if os.path.exists(input_path):
        with open(input_path, "r", encoding="utf-8") as file:
            return json.load(file)
    else:
        raise FileNotFoundError(f"Input file {input_path} not found.")

def extract_keywords(articles):
    """Extract keywords from articles using spaCy."""
    nlp = spacy.load("en_core_web_sm")
    all_keywords = []
    for article in articles:
        doc = nlp(article)
        keywords = [token.lemma_.lower() for token in doc if token.is_alpha and not token.is_stop]
        all_keywords.extend(keywords)
    return Counter(all_keywords)

def analyze_sentiment(articles):
    """Analyze sentiment of articles using NLTK."""
    download("vader_lexicon", quiet=True)
    sia = SentimentIntensityAnalyzer()
    sentiments = [sia.polarity_scores(article) for article in articles]
    avg_sentiment = {
        "positive": sum(s["pos"] for s in sentiments) / len(sentiments),
        "neutral": sum(s["neu"] for s in sentiments) / len(sentiments),
        "negative": sum(s["neg"] for s in sentiments) / len(sentiments),
    }
    return avg_sentiment

def generate_wordcloud(keywords, output_path):
    """Generate a word cloud from keywords."""
    wordcloud = WordCloud(width=800, height=400, background_color="white").generate_from_frequencies(keywords)
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    plt.savefig(output_path)
    plt.close()

def main():
    parser = argparse.ArgumentParser(description="AI Trend Analyzer")
    parser.add_argument("--input", required=True, help="Path to input JSON file containing articles.")
    parser.add_argument("--output", required=True, help="Path to save the output word cloud image.")
    args = parser.parse_args()

    try:
        data = load_input(args.input)
        if not isinstance(data, list) or not all(isinstance(article, str) for article in data):
            raise ValueError("Input file must contain a JSON array of strings.")

        keywords = extract_keywords(data)
        sentiment = analyze_sentiment(data)

        print("Top Keywords:")
        for word, count in keywords.most_common(10):
            print(f"{word}: {count}")

        print("\nSentiment Analysis:")
        for key, value in sentiment.items():
            print(f"{key.capitalize()}: {value:.2f}")

        generate_wordcloud(keywords, args.output)
        print(f"Word cloud saved to {args.output}")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()