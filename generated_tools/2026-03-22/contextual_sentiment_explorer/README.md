# Contextual Sentiment Explorer

## Overview

The Contextual Sentiment Explorer is a Python-based tool designed to analyze the sentiment of a given text while providing contextual insights about the most influential phrases or sentences. It uses advanced AI models to ensure a deeper understanding of sentiment nuances, making it ideal for NLP researchers or developers working on emotionally sensitive applications.

## Features

- Analyzes the sentiment of individual sentences in a given text.
- Provides sentiment labels (e.g., POSITIVE, NEGATIVE) and confidence scores.
- Displays results in a visually appealing table format using the `rich` library.

## Requirements

The tool requires the following Python packages:

- `transformers`
- `nltk`
- `rich`

You can install the required packages using pip:

```bash
pip install transformers nltk rich
```

## Usage

You can use the tool via the command line. Provide a text file as input or pipe text directly through standard input.

### Command Line Arguments

- `--input`: Path to the input text file. If not provided, the tool will read from standard input.

### Examples

#### Using an Input File

```bash
python contextual_sentiment_explorer.py --input example.txt
```

#### Using Standard Input

```bash
echo "I love this. But I hate that." | python contextual_sentiment_explorer.py
```

## Testing

The tool includes a test suite written with `pytest`. To run the tests, install `pytest` and execute:

```bash
pytest test_contextual_sentiment_explorer.py
```

The tests include:

1. Testing sentiment analysis for a single sentence.
2. Testing sentiment analysis for multiple sentences.
3. Testing the display of results in a table format.

## License

This project is licensed under the MIT License.
