# Dataset Tokenizer Benchmark

## Description
Dataset Tokenizer Benchmark is a Python tool designed to benchmark tokenization speed and memory consumption across multiple tokenizers on a given dataset. This tool helps AI developers choose the best tokenizer for preprocessing large datasets efficiently when training open-source LLMs.

## Features
- Supports popular tokenization libraries such as Hugging Face and SentencePiece.
- Reports tokenization speed and memory consumption.
- Handles large datasets with streaming and batching.

## Installation

```bash
pip install -r requirements.txt
```

## Usage

```bash
python dataset_tokenizer_benchmark.py --dataset data.txt --tokenizers hf_tokenizer sentencepiece
```

### Arguments
- `--dataset`: Path to the dataset file (text or JSONL).
- `--tokenizers`: List of tokenizer types (e.g., `hf_tokenizer`, `sentencepiece`).
- `--batch_size`: Batch size for tokenization (default: 100).

## Example

```bash
python dataset_tokenizer_benchmark.py --dataset sample.txt --tokenizers hf_gpt2 sentencepiece --batch_size 50
```

## Limitations
- Requires a valid SentencePiece model file for `sentencepiece` tokenizer.
- Tokenizer names for Hugging Face must be valid model identifiers.

## License
MIT License
