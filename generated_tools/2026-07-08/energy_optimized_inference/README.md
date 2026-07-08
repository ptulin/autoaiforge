# Energy-Optimized Inference Scheduler

## Description
The Energy-Optimized Inference Scheduler is a Python tool designed to minimize energy consumption during AI inference tasks. By dynamically monitoring hardware energy usage and optimizing batch sizes, this tool ensures efficient execution without sacrificing performance. It supports multi-GPU systems for distributed inference.

## Features
- Dynamically monitors hardware energy usage during inference.
- Optimizes batch sizes for energy-efficient execution.
- Supports multi-GPU systems for distributed inference.

## Installation
```bash
pip install -r requirements.txt
```

## Usage
```bash
python energy_optimized_inference.py --model my_model.pt --input data.npy --min_batch 16 --max_batch 64
```

## Example
1. Save your PyTorch model as `my_model.pt`.
2. Prepare your input data as a numpy array and save it as `data.npy`.
3. Run the tool:
```bash
python energy_optimized_inference.py --model my_model.pt --input data.npy --min_batch 16 --max_batch 64
```

## Requirements
- Python 3.8+
- torch==2.0.1
- psutil==5.9.6
- schedule==1.2.0
- numpy==1.24.3

## License
MIT License