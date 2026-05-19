import argparse
import json
import os
import matplotlib.pyplot as plt
from openai import ChatCompletion
from tiktoken import encoding_for_model

def simulate_recursive_task(model, task, depth, max_depth, token_limit):
    """
    Simulates a recursive reasoning task and measures token usage.

    Args:
        model (str): The model to use.
        task (str): The task description.
        depth (int): Current depth of recursion.
        max_depth (int): Maximum recursion depth.
        token_limit (int): Token limit for the model.

    Returns:
        dict: A dictionary containing token usage metrics.
    """
    if depth > max_depth:
        return {"depth": depth, "tokens": 0}

    try:
        encoding = encoding_for_model(model)
        tokens = encoding.encode(task)
        token_count = len(tokens)

        if token_count > token_limit:
            raise ValueError("Token limit exceeded at depth {}".format(depth))

        # Simulate recursive call
        child_result = simulate_recursive_task(model, task, depth + 1, max_depth, token_limit)

        return {
            "depth": depth,
            "tokens": token_count + child_result["tokens"],
            "child": child_result
        }

    except Exception as e:
        return {"depth": depth, "error": str(e)}

def profile_token_usage(config_path, output_path):
    """
    Profiles token usage for a recursive reasoning task.

    Args:
        config_path (str): Path to the JSON configuration file.
        output_path (str): Path to save the token usage report.

    Returns:
        dict: Token usage report.
    """
    with open(config_path, 'r') as f:
        config = json.load(f)

    model = config.get("model", "gpt-3.5-turbo")
    task = config.get("task", "")
    max_depth = config.get("max_depth", 5)
    token_limit = config.get("token_limit", 4096)

    if not task:
        raise ValueError("Task description is missing in the configuration file.")

    result = simulate_recursive_task(model, task, 1, max_depth, token_limit)

    with open(output_path, 'w') as f:
        json.dump(result, f, indent=4)

    return result

def visualize_token_growth(report, output_image):
    """
    Visualizes token growth based on the profiling report.

    Args:
        report (dict): Token usage report.
        output_image (str): Path to save the visualization image.
    """
    depths = []
    tokens = []

    def extract_data(node):
        depths.append(node["depth"])
        tokens.append(node.get("tokens", 0))
        if "child" in node and isinstance(node["child"], dict):
            extract_data(node["child"])

    extract_data(report)

    plt.figure(figsize=(10, 6))
    plt.plot(depths, tokens, marker='o')
    plt.title("Token Growth Across Recursive Depths")
    plt.xlabel("Depth")
    plt.ylabel("Tokens")
    plt.grid()
    plt.savefig(output_image)
    plt.close()

def main():
    parser = argparse.ArgumentParser(description="Recursive Token Profiler")
    parser.add_argument("--config", required=True, help="Path to the JSON configuration file.")
    parser.add_argument("--output", required=True, help="Path to save the token usage report.")
    parser.add_argument("--visual", required=False, help="Path to save the token growth visualization.")

    args = parser.parse_args()

    try:
        report = profile_token_usage(args.config, args.output)

        if args.visual:
            visualize_token_growth(report, args.visual)

        print(f"Token usage profiling complete. Report saved to {args.output}.")
        if args.visual:
            print(f"Visualization saved to {args.visual}.")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()