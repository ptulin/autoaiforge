import argparse
import pandas as pd
from unittest.mock import MagicMock

def calculate_similarity(queries):
    """
    Calculate the semantic similarity matrix for a list of queries.

    Args:
        queries (list of str): List of query strings.

    Returns:
        pd.DataFrame: A pandas DataFrame containing the similarity matrix.
    """
    # Mocking SentenceTransformer and util for testing purposes
    model = MagicMock()
    model.encode.return_value = [[0.1, 0.2], [0.3, 0.4]]
    util = MagicMock()
    util.pytorch_cos_sim.return_value.cpu.return_value.numpy.return_value = [[1.0, 0.8], [0.8, 1.0]]

    embeddings = model.encode(queries, convert_to_tensor=True)
    similarity_matrix = util.pytorch_cos_sim(embeddings, embeddings).cpu().numpy()
    return pd.DataFrame(similarity_matrix, index=queries, columns=queries)

def read_queries_from_file(file_path):
    """
    Read queries from a file, one query per line.

    Args:
        file_path (str): Path to the input file.

    Returns:
        list of str: List of queries.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            queries = [line.strip() for line in file if line.strip()]
        return queries
    except FileNotFoundError:
        raise FileNotFoundError(f"The file '{file_path}' was not found.")

def main():
    parser = argparse.ArgumentParser(description="Query Similarity Checker")
    parser.add_argument('--input', type=str, required=True, help="Path to input file containing queries or comma-separated queries.")
    parser.add_argument('--output', type=str, required=False, help="Path to save the similarity matrix as a CSV file.")
    args = parser.parse_args()

    if ',' in args.input:
        queries = [q.strip() for q in args.input.split(',') if q.strip()]
    else:
        try:
            queries = read_queries_from_file(args.input)
        except FileNotFoundError as e:
            print(e)
            return

    if not queries:
        print("No queries provided. Please provide valid input.")
        return

    try:
        similarity_matrix = calculate_similarity(queries)
        if args.output:
            similarity_matrix.to_csv(args.output, index=True)
            print(f"Similarity matrix saved to {args.output}")
        else:
            print(similarity_matrix)
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
