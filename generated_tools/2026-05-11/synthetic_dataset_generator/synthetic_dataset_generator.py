import argparse
import json
import pandas as pd
import openai
import os

def generate_synthetic_data(api_key, prompt, count, output_format):
    """
    Generate synthetic data using OpenAI's API.

    Args:
        api_key (str): OpenAI API key.
        prompt (str): Prompt template for data generation.
        count (int): Number of data samples to generate.
        output_format (str): Output format, either 'csv' or 'json'.

    Returns:
        str: Path to the output file containing the synthetic dataset.
    """
    if count <= 0:
        raise ValueError("Count must be a positive integer.")

    if output_format not in ['csv', 'json']:
        raise ValueError("Output format must be either 'csv' or 'json'.")

    openai.api_key = api_key

    data = []
    for _ in range(count):
        try:
            response = openai.Completion.create(
                engine="text-davinci-003",
                prompt=prompt,
                max_tokens=100
            )
            generated_text = response.choices[0].text.strip()
            data.append(generated_text)
        except Exception as e:
            raise RuntimeError(f"Error during data generation: {e}")

    output_file = f"synthetic_dataset.{output_format}"

    if output_format == 'json':
        with open(output_file, 'w') as f:
            json.dump(data, f, indent=4)
    elif output_format == 'csv':
        df = pd.DataFrame(data, columns=['Generated Data'])
        df.to_csv(output_file, index=False)

    return output_file

def main():
    parser = argparse.ArgumentParser(description="Synthetic Dataset Generator")
    parser.add_argument('--api_key', required=True, help="OpenAI API key")
    parser.add_argument('--prompt', required=True, help="Prompt template for data generation")
    parser.add_argument('--count', type=int, required=True, help="Number of data samples to generate")
    parser.add_argument('--output', required=True, choices=['csv', 'json'], help="Output file format (csv or json)")

    args = parser.parse_args()

    try:
        output_file = generate_synthetic_data(
            api_key=args.api_key,
            prompt=args.prompt,
            count=args.count,
            output_format=args.output
        )
        print(f"Synthetic dataset generated and saved to {output_file}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
