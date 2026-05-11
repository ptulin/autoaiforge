import argparse
import csv
import numpy as np
from scipy.spatial.distance import cosine
from tqdm import tqdm
import openai

def generate_responses(api_key, prompt, iterations):
    """Generate responses from the OpenAI model for the given prompt."""
    openai.api_key = api_key
    responses = []
    for _ in tqdm(range(iterations), desc="Generating responses"):
        try:
            response = openai.Completion.create(
                engine="text-davinci-003",
                prompt=prompt,
                max_tokens=100
            )
            responses.append(response.choices[0].text.strip())
        except Exception as e:
            print(f"Error generating response: {e}")
            responses.append("")
    return responses

def calculate_token_differences(responses):
    """Calculate token-level differences between responses."""
    token_sets = [set(response.split()) for response in responses]
    differences = []
    for i in range(len(token_sets)):
        for j in range(i + 1, len(token_sets)):
            diff = len(token_sets[i].symmetric_difference(token_sets[j]))
            differences.append(diff)
    return np.mean(differences), np.std(differences)

def calculate_semantic_similarity(responses):
    """Calculate semantic similarity using cosine distance."""
    embeddings = []
    for response in responses:
        try:
            embedding = openai.Embedding.create(input=response, model="text-embedding-ada-002")
            embeddings.append(embedding['data'][0]['embedding'])
        except Exception as e:
            print(f"Error generating embedding: {e}")
            embeddings.append([0] * 1536)  # Default embedding size for text-embedding-ada-002

    similarities = []
    for i in range(len(embeddings)):
        for j in range(i + 1, len(embeddings)):
            sim = 1 - cosine(embeddings[i], embeddings[j])
            similarities.append(sim)
    return np.mean(similarities), np.std(similarities)

def save_to_csv(output_file, metrics):
    """Save metrics to a CSV file."""
    with open(output_file, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Metric", "Mean", "Standard Deviation"])
        for metric, values in metrics.items():
            writer.writerow([metric, values[0], values[1]])

def main():
    parser = argparse.ArgumentParser(description="Model Stability Benchmark")
    parser.add_argument('--api_key', required=True, help="OpenAI API key")
    parser.add_argument('--prompt', required=True, help="Prompt text to evaluate")
    parser.add_argument('--iterations', type=int, required=True, help="Number of iterations")
    parser.add_argument('--output', required=True, help="Output CSV file path")

    args = parser.parse_args()

    responses = generate_responses(args.api_key, args.prompt, args.iterations)
    token_mean, token_std = calculate_token_differences(responses)
    semantic_mean, semantic_std = calculate_semantic_similarity(responses)

    metrics = {
        "Token Difference": (token_mean, token_std),
        "Semantic Similarity": (semantic_mean, semantic_std)
    }

    save_to_csv(args.output, metrics)
    print(f"Metrics saved to {args.output}")

if __name__ == "__main__":
    main()