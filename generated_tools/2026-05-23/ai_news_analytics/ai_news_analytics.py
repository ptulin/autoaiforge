import requests
from nltk.sentiment import SentimentIntensityAnalyzer
from nltk.tokenize import word_tokenize
from collections import Counter
import pandas as pd
import matplotlib.pyplot as plt
import argparse
import os
import re
import nltk

def fetch_article_content(url):
    """Fetch the content of an article from a given URL."""
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return None

def clean_text(text):
    """Clean and preprocess the text."""
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    text = text.lower()
    return text

def analyze_sentiment(texts):
    """Analyze sentiment and keyword frequency for a list of texts."""
    try:
        nltk.data.find('tokenizers/punkt')
    except LookupError:
        nltk.download('punkt')

    try:
        nltk.data.find('vader_lexicon')
    except LookupError:
        nltk.download('vader_lexicon')

    sia = SentimentIntensityAnalyzer()
    sentiments = []
    all_keywords = []

    for text in texts:
        cleaned_text = clean_text(text)
        if not cleaned_text:
            continue

        sentiment = sia.polarity_scores(cleaned_text)
        sentiments.append(sentiment)

        tokens = word_tokenize(cleaned_text)
        all_keywords.extend(tokens)

    keyword_freq = Counter(all_keywords)
    return sentiments, keyword_freq

def generate_sentiment_trend(sentiments, output_file):
    """Generate a sentiment trend graph and save it to a file."""
    df = pd.DataFrame(sentiments)
    df['index'] = range(len(df))

    plt.figure(figsize=(10, 6))
    plt.plot(df['index'], df['compound'], marker='o', label='Compound Sentiment')
    plt.axhline(0, color='red', linestyle='--', label='Neutral')
    plt.title('Sentiment Trend Over Time')
    plt.xlabel('Article Index')
    plt.ylabel('Compound Sentiment Score')
    plt.legend()
    plt.grid()
    plt.savefig(output_file)
    plt.close()

def main():
    parser = argparse.ArgumentParser(description="AI News Sentiment Analytics")
    parser.add_argument('--urls', nargs='+', help="List of article URLs to analyze.")
    parser.add_argument('--texts', nargs='+', help="List of article texts to analyze.")
    parser.add_argument('--output', default='sentiment_trend.png', help="Output file for sentiment trend graph.")

    args = parser.parse_args()

    if not args.urls and not args.texts:
        print("Error: You must provide either URLs or texts for analysis.")
        return

    texts = []

    if args.urls:
        for url in args.urls:
            content = fetch_article_content(url)
            if content:
                texts.append(content)

    if args.texts:
        texts.extend(args.texts)

    if not texts:
        print("Error: No valid texts to analyze.")
        return

    sentiments, keyword_freq = analyze_sentiment(texts)
    print("Sentiment Scores:", sentiments)
    print("Keyword Frequency:", keyword_freq.most_common(10))

    generate_sentiment_trend(sentiments, args.output)
    print(f"Sentiment trend graph saved to {args.output}")

if __name__ == "__main__":
    main()