# AI Model Profiler

AI Model Profiler is a CLI tool that analyzes pretrained AI models (e.g., PyTorch or TensorFlow models) to extract key insights such as layer distribution, parameter counts, and memory usage. This tool helps AI developers understand model architecture at a glance and optimize resource usage when deploying models.

## Features

- Analyze PyTorch models (.pt files) and TensorFlow models (.h5 files).
- Extract key insights such as layer distribution and total parameter counts.
- Generate a bar chart visualization of the layer distribution.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-repo/ai_model_profiler.git
   cd ai_model_profiler
   ```

2. Install the required dependencies:
   ```bash
   pip install torch tensorflow matplotlib
   ```

## Usage

Run the tool using the following command:

```bash
python ai_model_profiler.py --model <path_to_model> --output <output_json_path> [--chart <output_chart_path>]
```

### Arguments

- `--model`: Path to the pretrained model file (.pt for PyTorch or .h5 for TensorFlow).
- `--output`: Path to save the JSON report.
- `--chart`: (Optional) Path to save the visualization chart.

### Example

```bash
python ai_model_profiler.py --model model.pt --output analysis.json --chart chart.png
```

## Testing

To run the tests, install `pytest` and run:

```bash
pip install pytest
pytest test_ai_model_profiler.py
```

## License

This project is licensed under the MIT License.
