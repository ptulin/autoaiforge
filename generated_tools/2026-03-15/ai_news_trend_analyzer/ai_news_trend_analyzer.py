import argparse
import pandas as pd
import matplotlib.pyplot as plt
from textblob import TextBlob
from datetime import datetime

def analyze_trends(input_file, keywords):
    """
    Analyze the frequency and sentiment of keywords in the news articles.

    Args:
        input_file (str): Path to the CSV file containing news articles.
        keywords (list): List of keywords to analyze.

    Returns:
        dict: A dictionary containing frequency and sentiment data.
    """
    try:
        # Load the CSV file
        data = pd.read_csv(input_file)
    except Exception as e:
        raise ValueError(f"Error reading input file: {e}")

    if 'timestamp' not in data.columns or 'content' not in data.columns:
        raise ValueError("Input file must contain 'timestamp' and 'content' columns.")

    # Ensure timestamp is in datetime format
    data['timestamp'] = pd.to_datetime(data['timestamp'], errors='coerce')
    data = data.dropna(subset=['timestamp'])

    # Initialize results dictionary
    results = {}

    for keyword in keywords:
        keyword_data = data[data['content'].str.contains(keyword, case=False, na=False)]
        keyword_data['sentiment'] = keyword_data['content'].apply(lambda x: TextBlob(x).sentiment.polarity)

        # Group by date
        keyword_data['date'] = keyword_data['timestamp'].dt.date
        grouped = keyword_data.groupby('date').agg({
            'content': 'count',
            'sentiment': 'mean'
        }).rename(columns={'content': 'frequency', 'sentiment': 'average_sentiment'})

        results[keyword] = grouped

    return results

def plot_results(results, keywords):
    """
    Generate and display plots for the analysis results.

    Args:
        results (dict): The analysis results containing frequency and sentiment data.
        keywords (list): List of keywords analyzed.
    """
    for keyword in keywords:
        if keyword not in results:
            print(f"No data found for keyword: {keyword}")
            continue

        data = results[keyword]

        fig, ax1 = plt.subplots()

        # Plot frequency
        ax1.set_xlabel('Date')
        ax1.set_ylabel('Frequency', color='tab:blue')
        ax1.plot(data.index, data['frequency'], color='tab:blue', label='Frequency')
        ax1.tick_params(axis='y', labelcolor='tab:blue')

        # Plot sentiment
        ax2 = ax1.twinx()
        ax2.set_ylabel('Average Sentiment', color='tab:orange')
        ax2.plot(data.index, data['average_sentiment'], color='tab:orange', label='Sentiment')
        ax2.tick_params(axis='y', labelcolor='tab:orange')

        # Title and legend
        plt.title(f"Trend and Sentiment Analysis for '{keyword}'")
        fig.tight_layout()
        plt.legend(loc='upper left')
        plt.show()

def main():
    parser = argparse.ArgumentParser(description="AI News Trend Analyzer")
    parser.add_argument('--keywords', type=str, required=True, help="Comma-separated list of keywords to analyze.")
    parser.add_argument('--input', type=str, required=True, help="Path to the input CSV file containing news articles.")

    args = parser.parse_args()

    keywords = [kw.strip() for kw in args.keywords.split(',')]

    try:
        results = analyze_trends(args.input, keywords)
        plot_results(results, keywords)
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()