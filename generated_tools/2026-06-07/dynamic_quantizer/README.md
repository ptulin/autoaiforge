# Dynamic LLM Quantizer

## Description
Dynamic LLM Quantizer is a Python library designed for AI developers to dynamically apply quantization techniques to large language models (LLMs) while monitoring resource usage in real-time. It enables adaptive optimization for constrained environments by allowing developers to toggle between quantization levels at runtime.

## Features
- Real-time resource monitoring during quantization.
- Supports dynamic switching between quantization methods (GGUF, GPTQ, AWQ).
- Seamless integration with popular LLM libraries like Transformers.

## Installation

Install the required dependencies:

```bash
pip install torch==2.0.1 transformers==4.31.0 psutil==5.9.5
```

## Usage

### Example

```python
from dynamic_quantizer import quantify_model
from transformers import AutoModel

# Load a pre-trained model
model = AutoModel.from_pretrained("bert-base-uncased")

# Quantify the model using GPTQ method with resource monitoring
result = quantify_model(model, method='GPTQ', monitor_resources=True)

# Access the quantized model and resource stats
quantized_model = result['quantized_model']
resource_stats = result['resource_stats']
print("Quantization completed in", result['time_taken'], "seconds")
print("Resource stats:", resource_stats)
```

### CLI Usage

```bash
python dynamic_quantizer.py --model_name bert-base-uncased --method GPTQ --monitor_resources
```

## Limitations
- This library currently supports only three quantization methods: GGUF, GPTQ, and AWQ.
- The actual quantization logic is a placeholder and needs to be implemented for real-world use cases.

## License
MIT License