# Synthetic Dataset Generator

## Description
The Synthetic Dataset Generator is a Python tool that allows users to generate synthetic datasets using OpenAI's generative AI models. It is designed to help developers create custom datasets for training or fine-tuning machine learning models, with controls over the style, complexity, and diversity of the generated data.

## Features
- Generate synthetic datasets using OpenAI's GPT models.
- Specify the number of data samples to generate.
- Choose between JSON or CSV output formats.

## Installation

1. Clone the repository:
   ```bash
   git clone <repository_url>
   cd synthetic_dataset_generator
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

Run the script with the following command:

```bash
python synthetic_dataset_generator.py --api_key <your_openai_api_key> \
                                       --prompt "<your_prompt>" \
                                       --count <number_of_samples> \
                                       --output <csv_or_json>
```

### Arguments
- `--api_key`: Your OpenAI API key (required).
- `--prompt`: The prompt template for data generation (required).
- `--count`: The number of data samples to generate (required, must be a positive integer).
- `--output`: The output file format, either `csv` or `json` (required).

### Example

Generate 10 synthetic product descriptions in JSON format:

```bash
python synthetic_dataset_generator.py --api_key "your_openai_api_key" \
                                       --prompt "Generate a list of product descriptions" \
                                       --count 10 \
                                       --output json
```

## Testing

To run the tests, use `pytest`:

```bash
pytest test_synthetic_dataset_generator.py
```

The tests use mocking to simulate OpenAI API responses, so no network access is required.

## Requirements
- Python 3.7+
- `openai`
- `pandas`
- `pytest`

## License
This project is licensed under the MIT License.