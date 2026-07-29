# Latency Tuner

Latency Tuner is a Python tool designed to help AI developers optimize and tune their inference pipelines for lower latency. It benchmarks the key stages of an inference pipeline (e.g., pre-processing, model execution, post-processing) and identifies bottlenecks. It can also suggest tweaks to improve throughput and latency.

## Features
- Benchmark specific stages of an inference pipeline.
- Identify bottlenecks in the pipeline.
- Provide optimization suggestions for stages with high latency.

## Installation
This tool requires Python 3.7 or higher and the following Python package:
- `numpy`

You can install the required package using pip:
```bash
pip install numpy
```

## Usage
Run the tool from the command line:
```bash
python latency_tuner.py --script <path_to_inference_script> --stages <comma_separated_stage_names>
```

### Arguments
- `--script`: Path to the Python script containing the inference pipeline stages.
- `--stages`: Comma-separated list of stage function names to benchmark.

### Example
Suppose you have an inference script `inference.py` with the following content:
```python
def preprocess():
    pass

def model_inference():
    pass

def postprocess():
    pass
```

You can benchmark the stages as follows:
```bash
python latency_tuner.py --script inference.py --stages preprocess,model_inference,postprocess
```

## Testing
The tool includes a test suite using `pytest`. To run the tests, install `pytest` and execute:
```bash
pytest test_latency_tuner.py
```

## License
This project is licensed under the MIT License.