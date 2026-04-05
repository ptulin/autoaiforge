# LLM Efficiency Analyzer

The **LLM Efficiency Analyzer** is a command-line tool designed to help researchers and developers evaluate the trade-offs between computational resources and model performance for large language models (LLMs). By varying key hyperparameters such as input sequence length, model size, and batch size, the tool generates detailed reports and plots that highlight where performance gains begin to plateau. This helps guide decisions about resource allocation for training and inference.

## Features

- Evaluate compute vs. performance trade-offs for large language models.
- Support for varying key hyperparameters like sequence length and batch size.
- Generate detailed efficiency reports in CSV format.
- Create performance vs. compute time plots for visualization.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-repo/llm_efficiency_analyzer.git
   cd llm_efficiency_analyzer
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

Run the tool with the following command:

```bash
python llm_efficiency_analyzer.py --model <model_name> --dataset <dataset_path> \
    --seq_len_range <min_seq_len> <max_seq_len> \
    --batch_size_range <min_batch_size> <max_batch_size> \
    --output_dir <output_directory>
```

### Example

```bash
python llm_efficiency_analyzer.py --model gpt2 --dataset data.jsonl \
    --seq_len_range 128 512 --batch_size_range 16 64 --output_dir ./output
```

This will:
- Load the `gpt2` model from Hugging Face.
- Evaluate performance on the dataset `data.jsonl` by varying sequence lengths from 128 to 512 and batch sizes from 16 to 64.
- Save a CSV report to `./output/efficiency_report.csv`.
- Save a performance vs. sequence length plot to `./output/efficiency_plot.png`.

## Example Output

### Efficiency Report (CSV)
| seq_len | batch_size | compute_time | performance |
|---------|------------|--------------|-------------|
| 128     | 16         | 1.28         | 0.5         |
| 256     | 32         | 2.56         | 0.75        |

### Efficiency Plot

The tool generates a plot showing performance vs. sequence length for different batch sizes.

![Sample Plot](docs/sample_plot.png)

## Testing

To run the tests, install `pytest` and execute:

```bash
pytest test_llm_efficiency_analyzer.py
```

## License

This project is licensed under the MIT License.
