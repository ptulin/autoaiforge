# Query Similarity Checker

## Description

The Query Similarity Checker is a Python utility that calculates the semantic similarity between search queries using AI embeddings. This tool is particularly useful for developers building search engines or recommendation systems to detect overlapping or redundant queries.

## Features

- Reads queries from a file or a comma-separated string.
- Calculates a similarity matrix using AI embeddings.
- Outputs the similarity matrix to the console or saves it as a CSV file.

## Installation

Install the required dependencies using pip:

```bash
pip install pandas pytest
```

## Usage

Run the script using the command line:

```bash
python query_similarity_checker.py --input <input_file_or_queries> [--output <output_file>]
```

### Arguments

- `--input`: Path to the input file containing queries (one per line) or a comma-separated list of queries.
- `--output` (optional): Path to save the similarity matrix as a CSV file.

### Example

```bash
python query_similarity_checker.py --input "query1,query2,query3" --output similarity_matrix.csv
```

or

```bash
python query_similarity_checker.py --input queries.txt --output similarity_matrix.csv
```

## Testing

Run the tests using `pytest`:

```bash
pytest test_query_similarity_checker.py
```

The tests include:

1. Verifying the correctness of the similarity matrix calculation.
2. Checking the functionality of reading queries from a file.
3. Ensuring proper error handling for missing files.

## Notes

This tool uses mocked AI embedding and similarity calculation for demonstration purposes. Replace the mocked components with actual implementations (e.g., SentenceTransformer and util from `sentence-transformers`) for production use.
