# Learning Rate Finder

## Description

`learning_rate_finder` is a CLI tool that helps developers identify the optimal learning rate for fine-tuning large language models. By performing a learning rate range test, it generates a learning rate vs. loss plot to guide hyperparameter tuning.

## Installation

Install the required dependencies using pip:

```bash
pip install torch transformers matplotlib
```

## Usage

Run the tool from the command line with the following arguments:

```bash
python learning_rate_finder.py --model <model_name> --dataset <dataset_path> --range <lr_min> <lr_max> --output <output_plot>
```

### Arguments

- `--model`: The name of the Hugging Face model to use (e.g., `bert-base-uncased`).
- `--dataset`: Path to the dataset in JSONL format. Each line should be a JSON object with `text` and `label` fields.
- `--range`: The range of learning rates to test, specified as two numbers (e.g., `1e-5 1e-1`).
- `--output`: (Optional) The output file path for the learning rate vs. loss plot. Default is `lr_plot.png`.

## Example

```bash
python learning_rate_finder.py --model bert-base-uncased --dataset data.jsonl --range 1e-5 1e-1 --output lr_plot.png
```

This will generate a plot named `lr_plot.png` showing the loss as a function of the learning rate.

## Testing

To run the tests, install `pytest` and run:

```bash
pytest test_learning_rate_finder.py
```

The tests include:
- Loading a dataset from a JSONL file.
- Preparing data using a mocked tokenizer.
- Running the learning rate range test with mocked external dependencies.

## License

This project is licensed under the MIT License.