# Hallucination Corrector

## Overview
The Hallucination Corrector is a Python tool designed to identify potential hallucinations in LLM-generated outputs and suggest corrections by querying external APIs, such as Wikipedia. This tool is useful for developers aiming to ensure the factual accuracy of AI-generated responses in their applications.

## Features
- Detects hallucinations in AI-generated text.
- Suggests corrections based on reliable sources (e.g., Wikipedia).
- Handles edge cases such as empty input gracefully.

## Installation

Install the required dependencies using pip:

```bash
pip install wikipedia-api nltk pytest
```

Ensure NLTK resources are downloaded:

```bash
python -c "import nltk; nltk.download('punkt')"
```

## Usage

Run the tool from the command line:

```bash
python hallucination_corrector.py "Your LLM-generated text here"
```

Optional: Specify sources for validation (default is Wikipedia):

```bash
python hallucination_corrector.py "Your LLM-generated text here" --sources Wikipedia
```

## Testing

Run the tests using pytest:

```bash
pytest test_hallucination_corrector.py
```

## Example

Input:

```bash
python hallucination_corrector.py "This is a hallucinated sentence."
```

Output:

```json
{
    "original_text": "This is a hallucinated sentence.",
    "flagged_hallucinations": ["This is a hallucinated sentence."],
    "suggested_corrections": [
        {
            "sentence": "This is a hallucinated sentence.",
            "suggestion": "No reliable information found in the allowed sources."
        }
    ]
}
```

## License

This project is licensed under the MIT License.