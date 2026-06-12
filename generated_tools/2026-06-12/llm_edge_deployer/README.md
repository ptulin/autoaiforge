# LLM Edge Deployer

LLM Edge Deployer is a Python library and CLI tool designed to streamline the process of deploying optimized LLMs on edge hardware. It provides utilities to convert models to hardware-efficient formats like ONNX, export them, and run compatibility checks for edge accelerators such as NVIDIA TensorRT.

## Features

- Convert models to ONNX format.
- Check compatibility with edge devices (e.g., NVIDIA TensorRT, OpenVINO).
- Run test inference on ONNX models with sample input data.

## Installation

Install the required dependencies using pip:

```bash
pip install onnx onnxruntime optimum numpy pytest
```

## Usage

### CLI

Run the tool from the command line:

```bash
python llm_edge_deployer.py --input_model <path_to_model> \
                            --target_device <device_type> \
                            --test_sample <path_to_test_sample> \
                            --output_model <path_to_output_model>
```

- `--input_model`: Path to the optimized model file.
- `--target_device`: Target edge device type (e.g., `tensorrt`, `openvino`).
- `--test_sample`: Path to the test sample JSON file.
- `--output_model`: (Optional) Path to save the converted ONNX model. Default is `output_model.onnx`.

### Library

You can also use the tool as a Python library:

```python
from llm_edge_deployer import convert_to_onnx, check_device_compatibility, run_test_inference

# Convert model to ONNX
output_model_path = convert_to_onnx("path/to/input_model", "path/to/output_model.onnx")

# Check device compatibility
check_device_compatibility("tensorrt")

# Run test inference
result = run_test_inference("path/to/output_model.onnx", "path/to/test_sample.json")
print("Inference result:", result)
```

## Testing

Run the tests using pytest:

```bash
pytest test_llm_edge_deployer.py
```

## License

This project is licensed under the MIT License.
