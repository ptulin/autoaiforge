# GPT Power Profiler

## Description
The GPT Power Profiler is a command-line tool designed to profile the power consumption of GPT models (e.g., GPT-4, GPT-5) during API calls. It measures CPU and GPU utilization over time and generates actionable insights for optimizing energy efficiency. This tool is particularly useful for large-scale deployments in energy-conscious environments.

## Features
- Profiles energy consumption during GPT model inference.
- Real-time monitoring of CPU and GPU utilization.
- Generates detailed power usage graphs for analysis.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-repo/gpt_power_profiler.git
   cd gpt_power_profiler
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Command-line Usage

```bash
python gpt_power_profiler.py --models gpt-4,gpt-5 --prompts prompts.json
```

- `--models`: Comma-separated list of GPT models to profile (e.g., `gpt-4,gpt-5`).
- `--prompts`: Path to a JSON file containing an array of prompts.

### Example

1. Create a `prompts.json` file:
   ```json
   [
       "Hello, how are you?",
       "What is the capital of France?",
       "Tell me a joke."
   ]
   ```

2. Run the profiler:
   ```bash
   python gpt_power_profiler.py --models gpt-4 --prompts prompts.json
   ```

3. View the generated power usage graphs in the current directory.

## Testing

Run the tests using `pytest`:

```bash
pytest test_gpt_power_profiler.py
```

## Limitations
- GPU utilization is currently a placeholder and requires additional libraries for accurate monitoring.
- The tool assumes the presence of a battery for power usage monitoring.

## License
This project is licensed under the MIT License.
