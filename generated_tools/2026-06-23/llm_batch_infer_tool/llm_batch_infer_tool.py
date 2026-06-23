import argparse
import json
import time
from pathlib import Path
from typing import List, Union
from joblib import Parallel, delayed
from transformers import pipeline

# Constants
DEFAULT_BATCH_SIZE = 16
DEFAULT_PARALLEL = 4
MODEL_NAME = "gpt2"
TOKEN_LIMIT = 512

def load_input(file_path: str) -> Union[List[str], List[dict]]:
    """Load input data from a text or JSON file."""
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"Input file {file_path} does not exist.")

    if path.suffix == ".txt":
        with open(file_path, "r", encoding="utf-8") as f:
            return [line.strip() for line in f if line.strip()]
    elif path.suffix == ".json":
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    else:
        raise ValueError("Unsupported file format. Only .txt and .json are supported.")

def save_output(output: Union[List[str], List[dict]], output_path: str):
    """Save output data to a JSON file."""
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=4)

def chunk_input(data: List[str], batch_size: int) -> List[List[str]]:
    """Split input data into chunks of specified batch size."""
    return [data[i:i + batch_size] for i in range(0, len(data), batch_size)]

def process_batch(batch: List[str], model_pipeline) -> List[str]:
    """Process a single batch of inputs using the LLM pipeline."""
    return [result['generated_text'] for result in model_pipeline(batch, max_length=TOKEN_LIMIT)]

def batch_inference(input_data: List[str], batch_size: int, parallel: int) -> List[str]:
    """Perform batch inference using the specified batch size and parallelization."""
    model_pipeline = pipeline("text-generation", model=MODEL_NAME, tokenizer=MODEL_NAME, device=-1)
    chunks = chunk_input(input_data, batch_size)
    results = Parallel(n_jobs=parallel)(
        delayed(process_batch)(chunk, model_pipeline) for chunk in chunks
    )
    return [item for sublist in results for item in sublist]

def main():
    parser = argparse.ArgumentParser(
        description="LLM Batch Inference Tool: Process input data in batches for faster inference using large language models."
    )
    parser.add_argument("--input", required=True, help="Path to the input file (text or JSON).")
    parser.add_argument("--output", required=True, help="Path to save the output JSON file.")
    parser.add_argument("--batch_size", type=int, default=DEFAULT_BATCH_SIZE, help="Batch size for processing (default: 16).")
    parser.add_argument("--parallel", type=int, default=DEFAULT_PARALLEL, help="Number of parallel processes (default: 4).")

    args = parser.parse_args()

    try:
        input_data = load_input(args.input)
        if not input_data:
            raise ValueError("Input file is empty.")

        start_time = time.time()
        results = batch_inference(input_data, args.batch_size, args.parallel)
        end_time = time.time()

        output_data = {
            "results": results,
            "timing": {
                "total_time_seconds": end_time - start_time,
                "batch_size": args.batch_size,
                "parallel": args.parallel
            }
        }

        save_output(output_data, args.output)
        print(f"Processing completed. Results saved to {args.output}")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
