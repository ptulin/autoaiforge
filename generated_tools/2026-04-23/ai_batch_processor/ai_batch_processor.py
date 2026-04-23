import os
import argparse
import pandas as pd
from concurrent.futures import ThreadPoolExecutor, as_completed
from transformers import pipeline

def process_task(model_name, input_text):
    try:
        model = pipeline(task="text-generation", model=model_name)
        result = model(input_text, max_length=100, num_return_sequences=1)
        return result[0]['generated_text']
    except Exception as e:
        return f"Error processing task: {str(e)}"

def process_file(file_path, model_name):
    try:
        with open(file_path, 'r') as f:
            input_text = f.read()
        return process_task(model_name, input_text)
    except Exception as e:
        return f"Error reading file {file_path}: {str(e)}"

def batch_process(input_dir, output_dir, model_name, max_workers):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    input_files = [os.path.join(input_dir, f) for f in os.listdir(input_dir) if os.path.isfile(os.path.join(input_dir, f))]
    results = {}

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_file = {executor.submit(process_file, file, model_name): file for file in input_files}
        for future in as_completed(future_to_file):
            file = future_to_file[future]
            try:
                results[file] = future.result()
            except Exception as e:
                results[file] = f"Error: {str(e)}"

    for file, output in results.items():
        output_file = os.path.join(output_dir, os.path.basename(file) + '.out')
        with open(output_file, 'w') as f:
            f.write(output)

def main():
    parser = argparse.ArgumentParser(description="AI Batch Processor")
    parser.add_argument('--model', required=True, help="Name of the AI model to use (e.g., gpt-neo)")
    parser.add_argument('--input_dir', required=True, help="Directory containing input files")
    parser.add_argument('--output_dir', required=True, help="Directory to save output files")
    parser.add_argument('--max_workers', type=int, default=4, help="Maximum number of parallel workers")

    args = parser.parse_args()

    batch_process(args.input_dir, args.output_dir, args.model, args.max_workers)

if __name__ == "__main__":
    main()