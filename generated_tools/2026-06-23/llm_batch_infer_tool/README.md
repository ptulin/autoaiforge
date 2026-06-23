# LLM Batch Inference Tool

## Description
The LLM Batch Inference Tool is a command-line utility designed to optimize and batch process input data for faster inference using large language models (LLMs). It splits large input datasets into manageable chunks, respects token limits, and parallelizes inference requests for local LLMs, significantly reducing processing time.

## Features
- Supports text and JSON input files.
- Splits input data into manageable chunks based on a specified batch size.
- Performs parallelized inference using the Hugging Face `transformers` library.
- Saves the output in JSON format, including timing information.

## Requirements
- Python 3.7+
- `transformers` library
- `joblib` library
- `pytest` for testing

Install the required dependencies using pip:
```bash
pip install transformers joblib pytest
```

## Usage
Run the tool from the command line:
```bash
python llm_batch_infer_tool.py --input <input_file> --output <output_file> [--batch_size <batch_size>] [--parallel <parallel_processes>]
```

### Arguments
- `--input`: Path to the input file (text or JSON).
- `--output`: Path to save the output JSON file.
- `--batch_size`: (Optional) Batch size for processing. Default is 16.
- `--parallel`: (Optional) Number of parallel processes. Default is 4.

### Example
```bash
python llm_batch_infer_tool.py --input data/input.txt --output data/output.json --batch_size 8 --parallel 2
```

## Testing
Run the tests using `pytest`:
```bash
pytest test_llm_batch_infer_tool.py
```

The test suite includes tests for:
- Loading input from text and JSON files.
- Splitting input data into chunks.
- Mocked batch inference using a simulated LLM pipeline.

## Notes
- This tool uses the Hugging Face `transformers` library for LLM inference. Ensure you have the required model (e.g., `gpt2`) downloaded or accessible.
- The tool is designed to work offline with mocked tests, ensuring no network access is required during testing.
