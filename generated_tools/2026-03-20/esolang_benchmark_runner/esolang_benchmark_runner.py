import json
import time
import click
import pandas as pd
import openai
from typing import List, Dict

@click.command()
@click.option('--model', required=True, help='The OpenAI model to use (e.g., gpt-4).')
@click.option('--language', required=True, help='The target esoteric language (e.g., brainfuck, befunge).')
@click.option('--tasks', required=True, type=click.Path(exists=True), help='Path to the JSON file containing tasks.')
@click.option('--output', required=True, type=click.Path(), help='Path to save the output metrics (JSON or CSV).')
def main(model: str, language: str, tasks: str, output: str):
    """
    Executes EsoLang-Bench tasks using the specified LLM and generates performance metrics.
    """
    try:
        # Load tasks from the provided JSON file
        with open(tasks, 'r') as f:
            task_data = json.load(f)

        if not isinstance(task_data, list) or not all('prompt' in task for task in task_data):
            raise ValueError("Tasks file must be a JSON array of objects with a 'prompt' key.")

        results = []

        for task in task_data:
            prompt = task['prompt']
            expected_output = task.get('expected_output', '')

            start_time = time.time()
            try:
                # Call OpenAI API
                response = openai.ChatCompletion.create(
                    model=model,
                    messages=[{"role": "user", "content": prompt}]
                )
                generated_code = response['choices'][0]['message']['content']
                execution_time = time.time() - start_time

                # Measure accuracy (simple string comparison for now)
                accuracy = int(generated_code.strip() == expected_output.strip())

                results.append({
                    'prompt': prompt,
                    'generated_code': generated_code,
                    'expected_output': expected_output,
                    'accuracy': accuracy,
                    'execution_time': execution_time
                })

            except Exception as e:
                results.append({
                    'prompt': prompt,
                    'generated_code': None,
                    'expected_output': expected_output,
                    'accuracy': 0,
                    'execution_time': None,
                    'error': str(e)
                })

        # Validate output file extension
        if not output.endswith('.json') and not output.endswith('.csv'):
            raise ValueError("Output file must have a .json or .csv extension.")

        # Save results to the specified output file
        if output.endswith('.json'):
            with open(output, 'w') as f:
                json.dump(results, f, indent=4)
        elif output.endswith('.csv'):
            df = pd.DataFrame(results)
            df.to_csv(output, index=False)

        click.echo(f"Results saved to {output}")

    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        raise SystemExit(1)

if __name__ == "__main__":
    main()
