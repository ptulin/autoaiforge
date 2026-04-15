import feedparser
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from transformers import pipeline
from typing import List, Dict

def fetch_feed_entries(feed_urls: List[str]) -> List[str]:
    """
    Fetches and parses RSS feed entries from the provided URLs.

    Args:
        feed_urls (List[str]): List of RSS feed URLs.

    Returns:
        List[str]: List of news article titles and descriptions.
    """
    entries = []
    for url in feed_urls:
        try:
            feed = feedparser.parse(url)
            if 'entries' in feed:
                for entry in feed['entries']:
                    content = entry.get('title', '') + ' ' + entry.get('description', '')
                    entries.append(content.strip())
        except Exception as e:
            print(f"Error fetching or parsing feed {url}: {e}")
    return entries

def cluster_topics(documents: List[str], num_clusters: int = 5) -> Dict[int, List[str]]:
    """
    Clusters the given documents into topics using KMeans.

    Args:
        documents (List[str]): List of text documents to cluster.
        num_clusters (int): Number of clusters to form.

    Returns:
        Dict[int, List[str]]: A dictionary with cluster indices as keys and lists of documents as values.
    """
    if not documents:
        return {}

    vectorizer = TfidfVectorizer(stop_words='english')
    X = vectorizer.fit_transform(documents)

    kmeans = KMeans(n_clusters=num_clusters, random_state=42, n_init=10)
    kmeans.fit(X)

    clusters = {i: [] for i in range(num_clusters)}
    for idx, label in enumerate(kmeans.labels_):
        clusters[label].append(documents[idx])

    return clusters

def summarize_clusters(clusters: Dict[int, List[str]], summary_length: int = 50) -> Dict[int, str]:
    """
    Summarizes each cluster using an AI-based summarization model.

    Args:
        clusters (Dict[int, List[str]]): Dictionary of clustered documents.
        summary_length (int): Maximum length of the summary for each cluster.

    Returns:
        Dict[int, str]: A dictionary with cluster indices as keys and summaries as values.
    """
    summarizer = pipeline("summarization")
    summaries = {}

    for cluster_id, documents in clusters.items():
        combined_text = " ".join(documents)
        try:
            summary = summarizer(combined_text, max_length=summary_length, min_length=10, do_sample=False)
            summaries[cluster_id] = summary[0]['summary_text']
        except Exception as e:
            print(f"Error summarizing cluster {cluster_id}: {e}")
            summaries[cluster_id] = ""

    return summaries

def track_trends(feed_urls: List[str], num_clusters: int = 5, summary_length: int = 50) -> Dict[int, Dict[str, str]]:
    """
    Tracks emerging news trends by analyzing real-time updates across multiple sources.

    Args:
        feed_urls (List[str]): List of RSS feed URLs.
        num_clusters (int): Number of clusters to form.
        summary_length (int): Maximum length of the summary for each cluster.

    Returns:
        Dict[int, Dict[str, str]]: A dictionary with cluster indices as keys, containing topics and summaries.
    """
    entries = fetch_feed_entries(feed_urls)
    clusters = cluster_topics(entries, num_clusters=num_clusters)
    summaries = summarize_clusters(clusters, summary_length=summary_length)

    result = {}
    for cluster_id, documents in clusters.items():
        result[cluster_id] = {
            "topics": documents,
            "summary": summaries.get(cluster_id, "")
        }

    return result

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="News Trend Tracker")
    parser.add_argument("--feeds", nargs='+', required=True, help="List of RSS feed URLs.")
    parser.add_argument("--clusters", type=int, default=5, help="Number of clusters to form.")
    parser.add_argument("--summary_length", type=int, default=50, help="Maximum length of the summary for each cluster.")

    args = parser.parse_args()

    trends = track_trends(args.feeds, num_clusters=args.clusters, summary_length=args.summary_length)
    for cluster_id, data in trends.items():
        print(f"Cluster {cluster_id}:")
        print(f"Topics: {data['topics']}")
        print(f"Summary: {data['summary']}")
        print()