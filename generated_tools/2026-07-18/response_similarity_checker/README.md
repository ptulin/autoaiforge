# Response Similarity Checker

## Overview

`response_similarity_checker` is a Python library that evaluates the similarity of LLM-generated responses to a set of reference outputs using metrics like cosine similarity or BLEU. This tool is useful for developers who want to measure how closely an LLM's behavior aligns with expected responses, making it particularly helpful for fine-tuning and benchmarking.

## Features

- **Cosine Similarity**: Compare vector-based responses and references.
- **BLEU Score**: Compare text-based responses and references.

## Requirements

- Python 3.7+
- `numpy`
- `scipy`
- `nltk`
- `scikit-learn`

## Installation

Install the required dependencies using pip:

```bash
pip install numpy scipy nltk scikit-learn
```

## Usage

### CLI Usage

You can use the tool from the command line to evaluate the similarity of responses to references using the BLEU metric:

```bash
python response_similarity_checker.py --responses "The cat is on the mat." "The dog is in the house." \
    --references "The cat is on the mat." "The dog is inside the house." \
    --metric bleu
```

### Python Library Usage

You can also use the library programmatically:

```python
from response_similarity_checker import evaluate_similarity
import numpy as np

# Example 1: BLEU similarity
responses = ["The cat is on the mat.", "The dog is in the house."]
references = ["The cat is on the mat.", "The dog is inside the house."]
scores = evaluate_similarity(responses, references, metric='bleu')
print(scores)

# Example 2: Cosine similarity
responses = [np.array([1, 0, 0]), np.array([0, 1, 0])]
references = [np.array([1, 0, 0]), np.array([0, 1, 0])]
scores = evaluate_similarity(responses, references, metric='cosine')
print(scores)
```

## Testing

To run the tests, install `pytest` and run:

```bash
pytest test_response_similarity_checker.py
```

The tests include cases for BLEU and cosine similarity, as well as edge cases for invalid inputs and mismatched lengths.

## License

This project is licensed under the MIT License.