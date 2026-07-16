import argparse
import json
import os
import random
from typing import Callable, List
from transformers import pipeline
import importlib.util

def load_scoring_function(script_path: str) -> Callable:
    """Dynamically load the scoring function from a Python script."""
    if not os.path.exists(script_path):
        raise FileNotFoundError(f"Scoring script not found: {script_path}")

    spec = importlib.util.spec_from_file_location("scoring_module", script_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    if not hasattr(module, "score_prompt"):
        raise AttributeError("The scoring script must define a 'score_prompt' function.")

    return module.score_prompt

def generate_prompt_variations(base_prompt: str, num_variations: int = 5) -> List[str]:
    """Generate systematic variations of the base prompt."""
    variations = []
    for i in range(num_variations):
        variations.append(f"{base_prompt} (variation {i + 1})")
    return variations

def evaluate_prompts(prompts: List[str], model_name: str, scoring_function: Callable) -> List[dict]:
    """Evaluate each prompt using the model and scoring function."""
    model = pipeline("text-generation", model=model_name)
    results = []

    for prompt in prompts:
        try:
            response = model(prompt, max_length=50, num_return_sequences=1)[0]["generated_text"]
            score = scoring_function(prompt, response)
            results.append({"prompt": prompt, "response": response, "score": score})
        except Exception as e:
            results.append({"prompt": prompt, "response": None, "score": None, "error": str(e)})

    return results

def find_best_prompt(results: List[dict]) -> dict:
    """Find the best-performing prompt based on the score."""
    valid_results = [r for r in results if r["score"] is not None]
    if not valid_results:
        raise ValueError("No valid results to determine the best prompt.")

    return max(valid_results, key=lambda x: x["score"])

def main():
    parser = argparse.ArgumentParser(description="LLM Prompt Optimizer")
    parser.add_argument("--model", required=True, help="Name of the language model to use.")
    parser.add_argument("--base_prompt", required=True, help="Base prompt to optimize.")
    parser.add_argument("--scoring_script", required=True, help="Path to the scoring script.")
    parser.add_argument("--output_file", help="Optional file to save the evaluation report.")
    args = parser.parse_args()

    try:
        scoring_function = load_scoring_function(args.scoring_script)
        prompt_variations = generate_prompt_variations(args.base_prompt)
        results = evaluate_prompts(prompt_variations, args.model, scoring_function)
        best_prompt = find_best_prompt(results)

        report = {
            "best_prompt": best_prompt,
            "all_results": results
        }

        if args.output_file:
            with open(args.output_file, "w") as f:
                json.dump(report, f, indent=4)
            print(f"Evaluation report saved to {args.output_file}")
        else:
            print(json.dumps(report, indent=4))

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()