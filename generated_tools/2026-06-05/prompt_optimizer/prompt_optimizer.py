import argparse
import json
import os
import importlib.util
import pandas as pd
import numpy as np
import openai

def load_test_cases(file_path):
    """Load test cases from a JSON file."""
    try:
        with open(file_path, 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        raise ValueError(f"Error loading test cases: {e}")

def load_scorer(file_path):
    """Load scoring function from a Python script."""
    try:
        spec = importlib.util.spec_from_file_location("scorer", file_path)
        scorer_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(scorer_module)
        if not hasattr(scorer_module, 'score'):
            raise ValueError("Scorer script must define a 'score' function.")
        return scorer_module.score
    except Exception as e:
        raise ValueError(f"Error loading scorer script: {e}")

def generate_prompt_variations(base_prompt, placeholders):
    """Generate all possible prompt variations by replacing placeholders."""
    from itertools import product
    keys = list(placeholders.keys())
    values = [placeholders[key] for key in keys]
    variations = []

    for combination in product(*values):
        prompt = base_prompt
        for key, value in zip(keys, combination):
            prompt = prompt.replace(f"{{{key}}}", value)
        variations.append(prompt)

    return variations

def query_llm(prompt):
    """Query the OpenAI API with a prompt."""
    try:
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=100
        )
        return response.choices[0].text.strip()
    except Exception as e:
        return f"Error querying LLM: {e}"

def evaluate_prompts(prompts, test_cases, scorer):
    """Evaluate each prompt using the test cases and scoring function."""
    results = []

    for prompt in prompts:
        scores = []
        for test_case in test_cases:
            filled_prompt = prompt.format(**test_case)
            output = query_llm(filled_prompt)
            score = scorer(test_case, output)
            scores.append(score)

        avg_score = np.mean(scores)
        results.append({"prompt": prompt, "average_score": avg_score})

    return sorted(results, key=lambda x: x['average_score'], reverse=True)

def save_results(results, output_format, output_path):
    """Save results to a file in the specified format."""
    try:
        if output_format == "json":
            with open(output_path, 'w') as f:
                json.dump(results, f, indent=4)
        elif output_format == "csv":
            df = pd.DataFrame(results)
            df.to_csv(output_path, index=False)
        else:
            raise ValueError("Unsupported output format. Use 'json' or 'csv'.")
    except Exception as e:
        raise ValueError(f"Error saving results: {e}")

def main():
    parser = argparse.ArgumentParser(description="Prompt Optimizer")
    parser.add_argument("--prompt", required=True, help="Base prompt template with placeholders.")
    parser.add_argument("--test_cases", required=True, help="Path to JSON file containing test cases.")
    parser.add_argument("--scorer", required=True, help="Path to Python script defining scoring function.")
    parser.add_argument("--output_format", choices=["json", "csv"], default="json", help="Output format for results.")
    parser.add_argument("--output_path", default="results.json", help="Path to save the results.")
    args = parser.parse_args()

    try:
        test_cases = load_test_cases(args.test_cases)
        scorer = load_scorer(args.scorer)

        placeholders = {key: list(set(tc[key] for tc in test_cases if key in tc)) for key in test_cases[0].keys()}
        prompt_variations = generate_prompt_variations(args.prompt, placeholders)

        results = evaluate_prompts(prompt_variations, test_cases, scorer)
        save_results(results, args.output_format, args.output_path)
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()