import argparse
import time
import psutil
from transformers import AutoTokenizer
import sentencepiece as spm
from tqdm import tqdm
import json

def benchmark_tokenizer(dataset_path, tokenizer_types, batch_size=100):
    results = []

    # Load dataset
    try:
        with open(dataset_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    except FileNotFoundError:
        print(f"Error: File {dataset_path} not found.")
        return

    # Process tokenizers
    for tokenizer_type in tokenizer_types:
        print(f"Benchmarking tokenizer: {tokenizer_type}")

        if tokenizer_type.startswith("hf_"):
            tokenizer_name = tokenizer_type[3:]
            try:
                tokenizer = AutoTokenizer.from_pretrained(tokenizer_name)
            except Exception as e:
                print(f"Error loading Hugging Face tokenizer '{tokenizer_name}': {e}")
                continue
        elif tokenizer_type == "sentencepiece":
            try:
                sp = spm.SentencePieceProcessor()
                sp.Load("sentencepiece.model")  # Requires a SentencePiece model file
                tokenizer = sp
            except Exception as e:
                print(f"Error loading SentencePiece tokenizer: {e}")
                continue
        else:
            print(f"Unsupported tokenizer type: {tokenizer_type}")
            continue

        start_time = time.time()
        mem_before = psutil.Process().memory_info().rss

        tokenized_batches = []
        for i in tqdm(range(0, len(lines), batch_size), desc=f"Tokenizing with {tokenizer_type}"):
            batch = lines[i:i+batch_size]
            if isinstance(tokenizer, AutoTokenizer):
                tokenized_batches.append([tokenizer.tokenize(line) for line in batch])
            elif isinstance(tokenizer, spm.SentencePieceProcessor):
                tokenized_batches.append([tokenizer.EncodeAsPieces(line) for line in batch])

        mem_after = psutil.Process().memory_info().rss
        end_time = time.time()

        results.append({
            "tokenizer": tokenizer_type,
            "time_taken": end_time - start_time,
            "memory_used": mem_after - mem_before
        })

    return results


def main():
    parser = argparse.ArgumentParser(description="Dataset Tokenizer Benchmark")
    parser.add_argument("--dataset", required=True, help="Path to the dataset file (text or JSONL)")
    parser.add_argument("--tokenizers", nargs='+', required=True, help="List of tokenizer types (e.g., hf_tokenizer, sentencepiece)")
    parser.add_argument("--batch_size", type=int, default=100, help="Batch size for tokenization")

    args = parser.parse_args()

    results = benchmark_tokenizer(args.dataset, args.tokenizers, args.batch_size)

    if results:
        print("\nBenchmark Results:")
        for result in results:
            print(f"Tokenizer: {result['tokenizer']}")
            print(f"  Time Taken: {result['time_taken']:.2f} seconds")
            print(f"  Memory Used: {result['memory_used'] / (1024 * 1024):.2f} MB")


if __name__ == "__main__":
    main()
