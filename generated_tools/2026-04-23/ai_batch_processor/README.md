# AI Batch Processor

## Description
The AI Batch Processor is a Python tool designed for batch processing tasks using free AI models such as GPT-J or LLaMA. It is ideal for developers working on large-scale AI tasks like bulk text generation, translation, or summarization. The tool supports parallel processing, logging, and output aggregation.

## Features
- Batch processing for multiple input files or data entries
- Parallel execution to speed up processing
- Aggregated logging and configurable output formats

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/ai_batch_processor.git
   cd ai_batch_processor
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage
Run the script with the following arguments:
```bash
python ai_batch_processor.py --model gpt-neo --input_dir ./prompts --output_dir ./results
```

### Arguments
- `--model`: Name of the AI model to use (e.g., `gpt-neo`)
- `--input_dir`: Directory containing input files
- `--output_dir`: Directory to save output files
- `--max_workers`: Maximum number of parallel workers (default: 4)

## Example
```bash
python ai_batch_processor.py --model gpt-neo --input_dir ./prompts --output_dir ./results --max_workers 8
```

## Testing
Run the tests using pytest:
```bash
pytest test_ai_batch_processor.py
```

## License
MIT License