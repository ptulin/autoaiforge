import pandas as pd
import numpy as np
import argparse

def generate_dataset(vocab_size=100, num_samples=1000, sentence_length=10):
    """
    Generate a synthetic dataset of text samples.

    Parameters:
        vocab_size (int): Size of the vocabulary.
        num_samples (int): Number of samples to generate.
        sentence_length (int): Number of words per sentence.

    Returns:
        pd.DataFrame: A DataFrame containing the synthetic dataset.
    """
    if vocab_size <= 0 or num_samples <= 0 or sentence_length <= 0:
        raise ValueError("All parameters must be positive integers.")

    vocabulary = [f"word{i}" for i in range(vocab_size)]
    data = {
        "id": [],
        "text": []
    }

    for i in range(num_samples):
        sentence = " ".join(np.random.choice(vocabulary, sentence_length))
        data["id"].append(i)
        data["text"].append(sentence)

    return pd.DataFrame(data)

def custom_metric(dataset, metric_function):
    """
    Apply a custom metric function to the dataset.

    Parameters:
        dataset (pd.DataFrame): The dataset to evaluate.
        metric_function (function): A function that takes a text sample and returns a score.

    Returns:
        pd.DataFrame: A DataFrame with the original dataset and the metric scores.
    """
    if not isinstance(dataset, pd.DataFrame):
        raise ValueError("Dataset must be a pandas DataFrame.")

    if "text" not in dataset.columns:
        raise ValueError("Dataset must contain a 'text' column.")

    dataset = dataset.copy()
    dataset["score"] = dataset["text"].apply(metric_function)
    return dataset

def save_dataset(dataset, file_path, format="csv"):
    """
    Save the dataset to a file.

    Parameters:
        dataset (pd.DataFrame): The dataset to save.
        file_path (str): Path to the output file.
        format (str): File format ('csv' or 'json').

    Returns:
        None
    """
    if format == "csv":
        dataset.to_csv(file_path, index=False)
    elif format == "json":
        dataset.to_json(file_path, orient="records", lines=True)
    else:
        raise ValueError("Unsupported format. Use 'csv' or 'json'.")

def main():
    parser = argparse.ArgumentParser(description="Dataset & Metric Synthesizer")
    parser.add_argument("--vocab_size", type=int, default=100, help="Vocabulary size")
    parser.add_argument("--num_samples", type=int, default=1000, help="Number of samples")
    parser.add_argument("--sentence_length", type=int, default=10, help="Sentence length")
    parser.add_argument("--output_file", type=str, required=True, help="Output file path")
    parser.add_argument("--format", type=str, choices=["csv", "json"], default="csv", help="Output file format")

    args = parser.parse_args()

    dataset = generate_dataset(args.vocab_size, args.num_samples, args.sentence_length)
    save_dataset(dataset, args.output_file, args.format)

if __name__ == "__main__":
    main()
