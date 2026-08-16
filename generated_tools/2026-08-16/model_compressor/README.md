# Model Compressor
This tool reduces the size of AI models by applying techniques like quantization, knowledge distillation, and weight sharing.

## Installation
To install the required packages, run `pip install tensorflow torch`.

## Usage
To use the model compressor, run `python model_compressor.py --input_model input_model.h5 --compression_ratio 0.5 --output_model output_model.h5 --compression_algorithm quantization`.

## Supported Compression Algorithms
- Quantization
- Knowledge Distillation
- Weight Sharing