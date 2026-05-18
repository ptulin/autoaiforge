# Batch Text Summarizer

Batch Text Summarizer is a command-line tool that processes a batch of text files, summarizes their content using OpenAI's GPT-based API, and saves the summaries in a specified output directory. This tool is ideal for developers and researchers who need to efficiently summarize large datasets of textual information.

## Features

- Processes multiple text files in a single batch.
- Uses OpenAI's GPT-based API for high-quality text summarization.
- Configurable summary length with the `--max-tokens` parameter.
- Skips empty files automatically.
- Generates summaries with metadata for traceability.

## Installation

1. Clone the repository or download the script `batch_text_summarizer.py`.
2. Install the required dependencies:

```bash
pip install -r requirements.txt
```

## Usage

Run the script from the command line:

```bash
python batch_text_summarizer.py --input-dir ./texts --output-dir ./summaries --api-key YOUR_API_KEY
```

### Arguments

- `--input-dir`: Path to the directory containing text files to summarize.
- `--output-dir`: Path to the directory where summaries will be saved.
- `--api-key`: Your OpenAI API key for accessing the summarization model.
- `--max-tokens`: (Optional) Maximum number of tokens for the summary. Default is 100.

### Example

```bash
python batch_text_summarizer.py --input-dir ./texts --output-dir ./summaries --api-key sk-abc123 --max-tokens 150
```

## Testing

To run the tests, ensure you have `pytest` installed and run:

```bash
pytest test_batch_text_summarizer.py
```

The tests include:

1. Verifying the `summarize_text` function with a mocked OpenAI API response.
2. Testing the `process_files` function to ensure summaries are generated correctly.
3. Ensuring that empty files are skipped during processing.

## License

This project is licensed under the MIT License.
