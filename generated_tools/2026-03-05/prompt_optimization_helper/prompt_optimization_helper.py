import argparse
import openai
import pandas as pd
import os

def evaluate_prompts(base_prompt, variations, api_key):
    """
    Evaluate prompt variations using OpenAI API and return scores.

    Args:
        base_prompt (str): The base prompt to evaluate.
        variations (list): A list of prompt variations.
        api_key (str): OpenAI API key.

    Returns:
        pd.DataFrame: A dataframe containing prompt variations and their scores.
    """
    openai.api_key = api_key

    results = []

    for variation in variations:
        prompt = f"{base_prompt} {variation}"
        try:
            response = openai.Completion.create(
                engine="text-davinci-003",
                prompt=prompt,
                max_tokens=50
            )
            output = response["choices"][0]["text"].strip()

            # Example scoring: length of response as a proxy for relevance
            score = len(output)

            results.append({"Prompt Variation": variation, "Output": output, "Score": score})
        except Exception as e:
            results.append({"Prompt Variation": variation, "Output": "Error", "Score": 0})

    return pd.DataFrame(results)

def main():
    parser = argparse.ArgumentParser(
        description="Prompt Optimization Helper: Optimize and refine prompts for LLMs."
    )

    parser.add_argument(
        "--base", required=True, help="Base prompt to use for testing variations."
    )
    parser.add_argument(
        "--variations", required=True, help="Path to a text file containing prompt variations (one per line)."
    )
    parser.add_argument(
        "--output", required=True, help="Path to save the output CSV file."
    )
    parser.add_argument(
        "--key", required=True, help="OpenAI API key."
    )

    args = parser.parse_args()

    # Read variations from file
    if not os.path.exists(args.variations):
        print(f"Error: Variations file '{args.variations}' not found.")
        return

    with open(args.variations, "r") as file:
        variations = [line.strip() for line in file if line.strip()]

    if not variations:
        print("Error: No variations found in the provided file.")
        return

    # Evaluate prompts
    try:
        results_df = evaluate_prompts(args.base, variations, args.key)
    except Exception as e:
        print(f"Error during prompt evaluation: {e}")
        return

    # Save results to CSV
    try:
        results_df.to_csv(args.output, index=False)
        print(f"Results saved to {args.output}")
    except Exception as e:
        print(f"Error saving results to CSV: {e}")

if __name__ == "__main__":
    main()
