# Adaptive LLM Optimizer

## Description
The Adaptive LLM Optimizer is an automation tool designed to dynamically adjust inference settings for locally hosted large language models (LLMs). It profiles hardware capabilities and monitors real-time performance metrics to optimize settings such as batch size, precision (FP16/FP32), and threading. This ensures maximum throughput and minimal latency during inference.

## Features
- **Real-time performance monitoring**: Continuously evaluates inference performance metrics like latency and throughput.
- **Dynamic hardware profiling**: Detects CPU, GPU, and memory capabilities to tailor settings.
- **Automatic optimization**: Adjusts batch size, precision, and threading based on hardware and performance metrics.

## Installation
1. Clone this repository:
   ```bash
   git clone https://github.com/your-repo/adaptive-llm-optimizer.git
   cd adaptive-llm-optimizer
   ```
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage
Run the tool from the command line with the following options:
```bash
python adaptive_llm_optimizer.py --model_path model.pt --hardware cpu --initial_batch_size 32 --precision FP32
```

### Arguments
- `--model_path`: Path to the model file (required).
- `--hardware`: Hardware type (`cpu` or `gpu`) (required).
- `--initial_batch_size`: Initial batch size for inference (default: 32).
- `--precision`: Precision type (`FP16` or `FP32`) (default: FP32).

### Example
```bash
python adaptive_llm_optimizer.py --model_path model.pt --hardware gpu --initial_batch_size 64 --precision FP16
```

## Testing
Run the test suite using `pytest`:
```bash
pytest test_adaptive_llm_optimizer.py
```

## License
This project is licensed under the MIT License.
