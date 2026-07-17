# Feature Inspector for LLM Detection

## Overview

This Python tool extracts and visualizes key linguistic features (e.g., word frequency distributions, sentence lengths, entropy scores) to help analyze potential differences between human-written and LLM-generated text. This is useful for developers who want to understand the underlying characteristics of text data.

## Features

- Extracts linguistic features such as:
  - Number of sentences
  - Number of words
  - Average sentence length
  - Entropy score
  - Word frequency distribution
- Visualizes features using histograms and bar plots.

## Installation

Install the required dependencies using pip:

```bash
pip install pandas matplotlib seaborn nltk
```

## Usage

Run the script from the command line:

```bash
python feature_inspector_for_llm_detection.py <input_text_or_file> [--output <output_file_prefix>]
```

- `<input_text_or_file>`: Path to a text file or a string of text.
- `--output`: (Optional) Prefix for saving visualizations as image files. If not provided, visualizations will be displayed interactively.

## Example

```bash
python feature_inspector_for_llm_detection.py "This is a test. This is only a test." --output results
```

## Testing

Run the tests using `pytest`:

```bash
pytest test_feature_inspector_for_llm_detection.py
```

## License

This project is licensed under the MIT License.