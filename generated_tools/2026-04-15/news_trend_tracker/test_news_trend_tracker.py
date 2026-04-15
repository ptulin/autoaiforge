import pytest
from unittest.mock import patch
from news_trend_tracker import fetch_feed_entries, cluster_topics, summarize_clusters, track_trends

def test_fetch_feed_entries():
    with patch('feedparser.parse') as mock_parse:
        mock_parse.return_value = {
            'entries': [
                {'title': 'Title 1', 'description': 'Description 1'},
                {'title': 'Title 2', 'description': 'Description 2'}
            ]
        }
        feeds = ['https://example.com/rss']
        result = fetch_feed_entries(feeds)
        assert result == ['Title 1 Description 1', 'Title 2 Description 2']

def test_cluster_topics():
    documents = ["Apple releases new iPhone", "Samsung unveils new Galaxy", "Apple and Samsung compete"]
    clusters = cluster_topics(documents, num_clusters=2)
    assert len(clusters) == 2
    assert sum(len(docs) for docs in clusters.values()) == len(documents)

def test_summarize_clusters():
    clusters = {
        0: ["Apple releases new iPhone", "Apple announces new features"],
        1: ["Samsung unveils new Galaxy"]
    }
    with patch('news_trend_tracker.pipeline') as mock_pipeline:
        mock_summarizer = mock_pipeline.return_value
        mock_summarizer.side_effect = [
            [{'summary_text': 'Apple news summary.'}],
            [{'summary_text': 'Samsung news summary.'}]
        ]
        summaries = summarize_clusters(clusters, summary_length=50)
        assert summaries[0] == 'Apple news summary.'
        assert summaries[1] == 'Samsung news summary.'

def test_track_trends():
    with patch('news_trend_tracker.fetch_feed_entries') as mock_fetch, \
         patch('news_trend_tracker.summarize_clusters') as mock_summarize:

        mock_fetch.return_value = ["Apple releases new iPhone", "Samsung unveils new Galaxy"]
        mock_summarize.return_value = {0: "Apple summary", 1: "Samsung summary"}

        result = track_trends(['https://example.com/rss'], num_clusters=2, summary_length=50)

        assert len(result) == 2
        assert result[0]['summary'] == "Apple summary"
        assert result[1]['summary'] == "Samsung summary"
