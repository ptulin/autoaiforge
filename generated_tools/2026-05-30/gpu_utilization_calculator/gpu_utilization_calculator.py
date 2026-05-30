import argparse
import time
import torch
import matplotlib.pyplot as plt
import GPUtil
from torch import nn

def monitor_gpu_utilization(duration, interval, output_file):
    """
    Monitors GPU utilization over a specified duration and interval.

    Args:
        duration (int): Total duration to monitor in seconds.
        interval (float): Time interval between checks in seconds.
        output_file (str): Path to save the utilization graph.

    Returns:
        list: A list of GPU utilization percentages over time.
    """
    utilization = []
    timestamps = []
    start_time = time.time()

    while time.time() - start_time < duration:
        gpus = GPUtil.getGPUs()
        if gpus:
            utilization.append(gpus[0].load * 100)  # Assuming single GPU
        else:
            utilization.append(0)
        timestamps.append(time.time() - start_time)
        time.sleep(interval)

    # Plot and save the utilization graph
    plt.figure()
    plt.plot(timestamps, utilization, label='GPU Utilization (%)')
    plt.xlabel('Time (s)')
    plt.ylabel('Utilization (%)')
    plt.title('GPU Utilization Over Time')
    plt.legend()
    plt.savefig(output_file)
    plt.close()

    return utilization

def run_inference(model_name, input_text):
    """
    Runs inference on a specified model with input text.

    Args:
        model_name (str): Name of the model to use.
        input_text (str): Input text for inference.

    Returns:
        str: The output of the model inference.
    """
    try:
        model = torch.hub.load('huggingface/pytorch-transformers', 'model', model_name)
        tokenizer = torch.hub.load('huggingface/pytorch-transformers', 'tokenizer', model_name)
        inputs = tokenizer.encode(input_text, return_tensors='pt')
        outputs = model.generate(inputs, max_length=50)
        return tokenizer.decode(outputs[0], skip_special_tokens=True)
    except Exception as e:
        raise RuntimeError(f"Error during inference: {e}")

def main():
    parser = argparse.ArgumentParser(description="GPU Utilization Calculator for LLMs")
    parser.add_argument('--model', type=str, required=True, help="Name of the model to use (e.g., 'gpt-2').")
    parser.add_argument('--input_text', type=str, required=True, help="Input text for inference.")
    parser.add_argument('--duration', type=int, default=10, help="Duration to monitor GPU utilization (in seconds).")
    parser.add_argument('--interval', type=float, default=0.5, help="Interval between GPU utilization checks (in seconds).")
    parser.add_argument('--output_file', type=str, default='gpu_utilization.png', help="File to save the GPU utilization graph.")

    args = parser.parse_args()

    print(f"Running inference on model '{args.model}' with input text: {args.input_text}")
    try:
        inference_output = run_inference(args.model, args.input_text)
        print(f"Inference Output: {inference_output}")
    except RuntimeError as e:
        print(e)
        return

    print(f"Monitoring GPU utilization for {args.duration} seconds...")
    utilization = monitor_gpu_utilization(args.duration, args.interval, args.output_file)
    print(f"GPU Utilization Data: {utilization}")
    print(f"Utilization graph saved to {args.output_file}")

if __name__ == "__main__":
    main()