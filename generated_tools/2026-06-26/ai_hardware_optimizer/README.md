# AI Hardware Optimizer

AI Hardware Optimizer is a command-line tool designed to help AI developers optimize workloads by identifying the most efficient hardware configurations and settings for their specific models. This tool is particularly useful for resource-intensive tasks like large language model (LLM) inference.

## Features
- Automated exploration of hardware configurations
- Supports both CPU and GPU optimization parameters
- Produces actionable suggestions for optimal performance
- Outputs a ranked list of hardware configuration recommendations with performance metrics

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-repo/ai_hardware_optimizer.git
   cd ai_hardware_optimizer
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

Run the tool using the following command:

```bash
python ai_hardware_optimizer.py --model <model_name> --device <device> [--max_memory <max_memory>]
```

### Example

```bash
python ai_hardware_optimizer.py --model bert-base-uncased --device cuda --max_memory 8GB
```

### Arguments
- `--model`: Name of the model to optimize (e.g., `bert-base-uncased`).
- `--device`: Device to use (`cpu` or `cuda`).
- `--max_memory`: (Optional) Maximum memory allowed (e.g., `8GB`).

## Output

The tool outputs a ranked list of hardware configuration recommendations with performance metrics in a tabular format. For example:

```
+----+--------------+-----------------+--------+----------+
|    |   num_threads | mixed_precision | device |   time_ms |
+====+==============+=================+========+==========+
|  0 |            1 | False           | cpu    |     85.23 |
|  1 |            2 | False           | cpu    |     72.45 |
|  2 |            4 | False           | cpu    |     65.12 |
|  3 |            1 | True            | cpu    |     80.34 |
|  4 |            2 | True            | cpu    |     68.78 |
|  5 |            4 | True            | cpu    |     60.89 |
+----+--------------+-----------------+--------+----------+
```

## Testing

Run the tests using pytest:

```bash
pytest test_ai_hardware_optimizer.py
```

## License

MIT License
