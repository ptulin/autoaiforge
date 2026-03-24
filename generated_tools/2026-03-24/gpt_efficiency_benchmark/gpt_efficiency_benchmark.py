import argparse
import json
import time
import psutil
import matplotlib.pyplot as plt
from openai import ChatCompletion

def benchmark_model(model, prompts):
    """Benchmark a single GPT model with given prompts."""
    results = []
    for prompt in prompts:
        start_time = time.time()
        try:
            response = ChatCompletion.create(model=model, messages=[{"role": "user", "content": prompt}])
        except Exception as e:
            results.append({"prompt": prompt, "error": str(e)})
            continue

        end_time = time.time()
        latency = end_time - start_time
        memory = psutil.virtual_memory().used / (1024 ** 2)  # Memory in MB
        token_count = len(response.choices[0].message.content.split())

        results.append({
            "prompt": prompt,
            "latency": latency,
            "memory": memory,
            "token_count": token_count
        })
    return results

def generate_report(results, models, output_path):
    """Generate a visual performance comparison report."""
    latencies = {model: [res["latency"] for res in results[model] if "latency" in res] for model in models}
    memories = {model: [res["memory"] for res in results[model] if "memory" in res] for model in models}
    token_counts = {model: [res["token_count"] for res in results[model] if "token_count" in res] for model in models}

    plt.figure(figsize=(10, 6))
    for model in models:
        plt.plot(latencies[model], label=f"{model} Latency")
    plt.xlabel("Prompt Index")
    plt.ylabel("Latency (s)")
    plt.title("Latency Comparison")
    plt.legend()
    plt.savefig(output_path.replace(".html", "_latency.png"))

    plt.figure(figsize=(10, 6))
    for model in models:
        plt.plot(memories[model], label=f"{model} Memory Usage")
    plt.xlabel("Prompt Index")
    plt.ylabel("Memory (MB)")
    plt.title("Memory Usage Comparison")
    plt.legend()
    plt.savefig(output_path.replace(".html", "_memory.png"))

    plt.figure(figsize=(10, 6))
    for model in models:
        plt.plot(token_counts[model], label=f"{model} Token Throughput")
    plt.xlabel("Prompt Index")
    plt.ylabel("Tokens")
    plt.title("Token Throughput Comparison")
    plt.legend()
    plt.savefig(output_path.replace(".html", "_tokens.png"))

    with open(output_path, "w") as f:
        f.write(f"<html><body><h1>GPT Efficiency Benchmark Report</h1>")
        f.write(f"<h2>Latency Comparison</h2><img src='{output_path.replace('.html', '_latency.png')}'><br>")
        f.write(f"<h2>Memory Usage Comparison</h2><img src='{output_path.replace('.html', '_memory.png')}'><br>")
        f.write(f"<h2>Token Throughput Comparison</h2><img src='{output_path.replace('.html', '_tokens.png')}'><br>")
        f.write("</body></html>")

def main():
    parser = argparse.ArgumentParser(description="GPT Efficiency Benchmark")
    parser.add_argument("--models", required=True, help="Comma-separated list of models to benchmark")
    parser.add_argument("--prompts", required=True, help="Path to JSON file containing prompts")
    parser.add_argument("--output", required=True, help="Path to output HTML report")
    args = parser.parse_args()

    models = args.models.split(",")
    try:
        with open(args.prompts, "r") as f:
            prompts = json.load(f)
    except Exception as e:
        print(f"Error reading prompts file: {e}")
        return

    results = {}
    for model in models:
        results[model] = benchmark_model(model, prompts)

    generate_report(results, models, args.output)

if __name__ == "__main__":
    main()