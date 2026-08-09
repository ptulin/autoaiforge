import argparse
import json
import spacy
from sklearn.cluster import KMeans
from sklearn.feature_extraction.text import TfidfVectorizer

try:
    spacy.load('en_core_web_sm')
except OSError:
    print("Downloading language model for the spaCy 'en_core_web_sm'")
    spacy.cli.download("en_core_web_sm")

def load_data(input_file):
    try:
        with open(input_file, 'r') as f:
            queries = [line.strip() for line in f.readlines()]
        return queries
    except FileNotFoundError:
        print(f"File {input_file} not found.")
        return []

def extract_intents(queries):
    nlp = spacy.load('en_core_web_sm')
    vectorizer = TfidfVectorizer()
    if not queries:
        return {}
    vectors = vectorizer.fit_transform(queries)
    kmeans = KMeans(n_clusters=min(5, len(queries)))
    kmeans.fit(vectors)
    labels = kmeans.labels_
    intents = {}
    for i, label in enumerate(labels):
        if label not in intents:
            intents[label] = []
        intents[label].append(queries[i])
    return intents

def extract_keywords(intents):
    nlp = spacy.load('en_core_web_sm')
    keywords = {}
    for label, queries in intents.items():
        doc = nlp(' '.join(queries))
        keywords[label] = [token.text for token in doc if token.pos_ == 'NOUN']
    return keywords

def main(input_file, output_file):
    queries = load_data(input_file)
    intents = extract_intents(queries)
    keywords = extract_keywords(intents)
    with open(output_file, 'w') as f:
        json.dump(keywords, f)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Intent Discovery Tool')
    parser.add_argument('--input_file', required=True, help='Input file containing user queries')
    parser.add_argument('--output_file', required=True, help='Output file for discovered intents and keywords')
    args = parser.parse_args()
    main(args.input_file, args.output_file)