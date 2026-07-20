import argparse
import os
import requests
import yaml
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
from flask import Flask, request, jsonify

def detect_hardware():
    """Detect available hardware (CPU/GPU)."""
    if torch.cuda.is_available():
        return "cuda"
    return "cpu"

def download_model(model_name, precision):
    """Download the specified model and tokenizer."""
    try:
        print(f"Downloading model {model_name}...")
        model = AutoModelForCausalLM.from_pretrained(model_name, torch_dtype=torch.float16 if precision == "fp16" else torch.float32)
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        return model, tokenizer
    except Exception as e:
        raise RuntimeError(f"Failed to download model {model_name}: {e}")

def start_server(model, tokenizer, device):
    """Start a local inference server."""
    app = Flask(__name__)

    @app.route("/generate", methods=["POST"])
    def generate():
        data = request.json
        prompt = data.get("prompt", "")
        if not prompt:
            return jsonify({"error": "Prompt is required"}), 400
        inputs = tokenizer(prompt, return_tensors="pt").to(device)
        outputs = model.generate(**inputs)
        response = tokenizer.decode(outputs[0], skip_special_tokens=True)
        return jsonify({"response": response})

    app.run(host="0.0.0.0", port=5000)

def main():
    parser = argparse.ArgumentParser(description="LLM Quickstart: Automate LLM setup and deployment.")
    parser.add_argument("--model", required=True, help="Model name, e.g., 'EleutherAI/gpt-j-6B'")
    parser.add_argument("--precision", choices=["fp32", "fp16"], default="fp32", help="Precision for model weights")
    parser.add_argument("--server", action="store_true", help="Start a local inference server")

    args = parser.parse_args()

    device = detect_hardware()
    print(f"Detected hardware: {device}")

    try:
        model, tokenizer = download_model(args.model, args.precision)
        model.to(device)
    except RuntimeError as e:
        print(e)
        return

    if args.server:
        start_server(model, tokenizer, device)
    else:
        print("Model downloaded and ready for local inference.")

if __name__ == "__main__":
    main()
