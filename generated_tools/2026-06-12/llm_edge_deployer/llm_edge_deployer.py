import argparse
import os
import json
import numpy as np
import onnx
import onnxruntime as ort
from optimum.onnxruntime import ORTModel

def convert_to_onnx(input_model_path, output_model_path):
    """Convert the input model to ONNX format."""
    try:
        model = ORTModel.from_pretrained(input_model_path)
        model.save_pretrained(output_model_path)
        return output_model_path
    except Exception as e:
        raise RuntimeError(f"Failed to convert model to ONNX: {e}")

def check_device_compatibility(target_device):
    """Check compatibility of the target device."""
    supported_devices = ["tensorrt", "openvino"]
    if target_device.lower() not in supported_devices:
        raise ValueError(f"Unsupported target device: {target_device}. Supported devices are: {supported_devices}")
    return True

def run_test_inference(onnx_model_path, test_sample_path):
    """Run a test inference on the ONNX model."""
    try:
        session = ort.InferenceSession(onnx_model_path)
        with open(test_sample_path, "r") as f:
            test_sample = json.load(f)
        input_name = session.get_inputs()[0].name
        input_data = np.array(test_sample, dtype=np.float32)
        result = session.run(None, {input_name: input_data})
        return [np.array(r) for r in result]  # Ensure result is a list of numpy arrays
    except Exception as e:
        raise RuntimeError(f"Failed to run test inference: {e}")

def main():
    parser = argparse.ArgumentParser(description="LLM Edge Deployer")
    parser.add_argument("--input_model", required=True, help="Path to the optimized model file.")
    parser.add_argument("--target_device", required=True, help="Target edge device type (e.g., tensorrt, openvino).")
    parser.add_argument("--test_sample", required=True, help="Path to the test sample JSON file.")
    parser.add_argument("--output_model", default="output_model.onnx", help="Path to save the converted ONNX model.")

    args = parser.parse_args()

    try:
        check_device_compatibility(args.target_device)
        print(f"Target device {args.target_device} is compatible.")

        output_model_path = convert_to_onnx(args.input_model, args.output_model)
        print(f"Model converted to ONNX format and saved at {output_model_path}.")

        inference_result = run_test_inference(output_model_path, args.test_sample)
        print(f"Test inference result: {inference_result}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
