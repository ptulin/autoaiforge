# Dataset Metric Synthesizer

This Python tool allows AI developers to create synthetic benchmarking datasets and evaluation metrics suited to specific tasks. It supports generating text-based datasets with controlled complexity and defining custom scoring functions for evaluating LLMs.

## Features

- Generate synthetic text datasets with configurable vocabulary size, number of samples, and sentence length.
- Apply custom metric functions to evaluate datasets.
- Save datasets in CSV or JSON format.

## Installation

Install the required dependencies using pip:

```bash
pip install pandas numpy
```

## Usage

### Command Line Interface

Run the tool from the command line:

```bash
python dataset_metric_synthesizer.py --vocab_size 100 --num_samples 1000 --sentence_length 10 --output_file output.csv --format csv
```

### Programmatic Usage

#### Generate a Dataset

```python
from dataset_metric_synthesizer import generate_dataset

dataset = generate_dataset(vocab_size=50, num_samples=10, sentence_length=5)
print(dataset.head())
```

#### Apply a Custom Metric

```python
from dataset_metric_synthesizer import custom_metric

def mock_metric(text):
    return len(text.split())

scored_dataset = custom_metric(dataset, mock_metric)
print(scored_dataset.head())
```

#### Save a Dataset

```python
from dataset_metric_synthesizer import save_dataset

save_dataset(dataset, "output.csv", format="csv")
```

## Testing

Run the tests using pytest:

```bash
pytest test_dataset_metric_synthesizer.py
```

## License

This project is licensed under the MIT License.