import argparse
import time
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from datasets import Dataset

def quantize_model(model, method):
    """Apply quantization to the model."""
    if method == "INT8":
        model = torch.quantization.quantize_dynamic(model, {torch.nn.Linear}, dtype=torch.qint8)
    elif method == "FP16":
        model = model.half()
    else:
        raise ValueError("Unsupported quantization method. Choose 'INT8' or 'FP16'.")
    return model

def evaluate_model(model, tokenizer, dataset, device):
    """Evaluate the model's accuracy on the given dataset."""
    model.to(device)
    model.eval()

    correct = 0
    total = 0

    for example in dataset:
        input_text = example['question']
        expected_answer = example['answers']['text'][0]

        inputs = tokenizer(input_text, return_tensors="pt").to(device)
        with torch.no_grad():
            outputs = model.generate(**inputs)

        generated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
        if expected_answer.lower() in generated_text.lower():
            correct += 1
        total += 1

    accuracy = correct / total if total > 0 else 0
    return accuracy

def benchmark_model(model, tokenizer, dataset, device):
    """Benchmark the model's speed and memory usage."""
    model.to(device)
    model.eval()

    start_time = time.time()
    if device == "cuda":
        torch.cuda.reset_peak_memory_stats(device)

    for example in dataset:
        input_text = example['question']
        inputs = tokenizer(input_text, return_tensors="pt").to(device)
        with torch.no_grad():
            model.generate(**inputs)

    elapsed_time = time.time() - start_time
    peak_memory = 0
    if device == "cuda":
        peak_memory = torch.cuda.max_memory_allocated(device) / (1024 ** 2)  # Convert to MB

    return elapsed_time, peak_memory

def main():
    parser = argparse.ArgumentParser(description="LLM Quantization Evaluator")
    parser.add_argument('--model', required=True, help="Name of the model (e.g., gpt2)")
    parser.add_argument('--quantization', required=True, choices=['INT8', 'FP16'], help="Quantization method")
    parser.add_argument('--dataset', required=True, help="Name of the evaluation dataset (e.g., squad)")
    parser.add_argument('--device', required=True, choices=['cpu', 'cuda'], help="Hardware device")

    args = parser.parse_args()

    # Load model and tokenizer
    print("Loading model and tokenizer...")
    model = AutoModelForCausalLM.from_pretrained(args.model)
    tokenizer = AutoTokenizer.from_pretrained(args.model)

    # Quantize model
    print(f"Applying {args.quantization} quantization...")
    model = quantize_model(model, args.quantization)

    # Load dataset
    print("Loading dataset...")
    dataset = Dataset.from_dict({
        "question": ["What is AI?"],
        "answers": [{"text": ["Artificial Intelligence"]}]
    })

    # Evaluate accuracy
    print("Evaluating model accuracy...")
    accuracy = evaluate_model(model, tokenizer, dataset, args.device)

    # Benchmark performance
    print("Benchmarking model performance...")
    elapsed_time, peak_memory = benchmark_model(model, tokenizer, dataset, args.device)

    # Output results
    print("Evaluation Results:")
    print(f"Accuracy: {accuracy:.2f}")
    print(f"Inference Time: {elapsed_time:.2f} seconds")
    print(f"Peak Memory Usage: {peak_memory:.2f} MB")

if __name__ == "__main__":
    main()
