# GPU Utilization Calculator for LLMs

## Description
The GPU Utilization Calculator for LLMs is a command-line tool designed to monitor GPU utilization in real-time during large language model (LLM) inference. It provides insights into how efficiently GPU resources are being used and generates a graphical visualization of GPU utilization over time. The tool also alerts users to potential underutilization or overutilization scenarios, enabling developers to optimize their configurations for better performance.

## Features
- Real-time GPU utilization monitoring during LLM inference.
- Graphical visualization of GPU utilization over time.
- Alerts for underutilization or overload scenarios.

## Installation

1. Clone the repository:
   ```bash
   git clone <repository_url>
   cd <repository_directory>
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

Run the tool using the following command:

```bash
python gpu_utilization_calculator.py --model gpt-2 --input_text 'Hello, world!' --duration 10 --interval 0.5 --output_file gpu_utilization.png
```

### Arguments
- `--model`: Name of the model to use (e.g., `gpt-2`).
- `--input_text`: Input text for inference.
- `--duration`: Duration to monitor GPU utilization (in seconds). Default is 10 seconds.
- `--interval`: Interval between GPU utilization checks (in seconds). Default is 0.5 seconds.
- `--output_file`: File to save the GPU utilization graph. Default is `gpu_utilization.png`.

## Example

```bash
python gpu_utilization_calculator.py --model gpt-2 --input_text 'Hello, world!'
```

This command will run inference on the `gpt-2` model with the input text `Hello, world!`, monitor GPU utilization for 10 seconds, and save the utilization graph as `gpu_utilization.png`.

## Testing

To run the tests, use the following command:

```bash
pytest test_gpu_utilization_calculator.py
```

All external network calls are mocked to ensure tests run without requiring network access.

## License

This project is licensed under the MIT License.