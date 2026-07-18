import numpy as np
from scipy.spatial.distance import cosine
from nltk.translate.bleu_score import sentence_bleu, SmoothingFunction
from sklearn.metrics.pairwise import cosine_similarity
from typing import List, Union

def evaluate_similarity(responses: List[Union[str, np.ndarray]], 
                        references: List[Union[str, np.ndarray]], 
                        metric: str = 'cosine') -> List[float]:
    """
    Evaluate the similarity between LLM responses and reference texts or vectors.

    Args:
        responses (List[Union[str, np.ndarray]]): A list of responses (strings or vectors).
        references (List[Union[str, np.ndarray]]): A list of reference texts (strings or vectors).
        metric (str): The similarity metric to use. Options: 'cosine', 'bleu'.

    Returns:
        List[float]: A list of similarity scores for each response-reference pair.
    """
    if len(responses) != len(references):
        raise ValueError("The number of responses and references must be equal.")

    if metric not in {'cosine', 'bleu'}:
        raise ValueError("Supported metrics are 'cosine' and 'bleu'.")

    scores = []

    for response, reference in zip(responses, references):
        if metric == 'cosine':
            if not isinstance(response, np.ndarray) or not isinstance(reference, np.ndarray):
                raise ValueError("Cosine similarity requires vector inputs, not strings.")
            if len(response) != len(reference):
                raise ValueError("Vectors for cosine similarity must have the same dimensions.")
            score = 1 - cosine(response, reference)
        elif metric == 'bleu':
            if not isinstance(response, str) or not isinstance(reference, str):
                raise ValueError("BLEU score requires string inputs, not vectors.")
            reference_tokens = reference.split()
            response_tokens = response.split()
            smoothing_function = SmoothingFunction().method1
            score = sentence_bleu([reference_tokens], response_tokens, smoothing_function=smoothing_function)
        else:
            raise ValueError(f"Unsupported metric: {metric}")

        scores.append(score)

    return scores

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Response Similarity Checker")
    parser.add_argument("--responses", nargs='+', required=True, help="List of LLM responses.")
    parser.add_argument("--references", nargs='+', required=True, help="List of reference texts.")
    parser.add_argument("--metric", choices=['cosine', 'bleu'], default='bleu', help="Similarity metric to use.")

    args = parser.parse_args()

    responses = args.responses
    references = args.references
    metric = args.metric

    if metric == 'cosine':
        raise ValueError("Cosine similarity cannot be used with CLI inputs as they are treated as strings.")

    scores = evaluate_similarity(responses, references, metric)

    for i, score in enumerate(scores):
        print(f"Response {i + 1}: Similarity Score = {score:.4f}")