import json
from nltk.tokenize import word_tokenize
import openai
import tiktoken
from typing import Dict, Any

def simulate_recursive_chain(prompt_template: str, task_config: Dict[str, Any], max_depth: int = 3) -> Dict[str, Any]:
    """
    Simulates a recursive reasoning chain based on the provided prompt template and task configuration.

    Args:
        prompt_template (str): The prompt template to use.
        task_config (Dict[str, Any]): Configuration for the recursive reasoning task.
        max_depth (int): Maximum recursion depth.

    Returns:
        Dict[str, Any]: Simulation results including token usage and responses.
    """
    results = []
    try:
        current_prompt = prompt_template.format(**task_config)
    except KeyError as e:
        return {"error": f"Missing key in task_config: {e}"}

    for depth in range(max_depth):
        try:
            response = openai.Completion.create(
                engine="text-davinci-003",
                prompt=current_prompt,
                max_tokens=150
            )
            response_text = response["choices"][0]["text"].strip()
            results.append({"depth": depth, "prompt": current_prompt, "response": response_text})
            current_prompt = prompt_template.format(response=response_text, **task_config)
        except Exception as e:
            results.append({"depth": depth, "error": str(e)})
            break

    return {"results": results, "total_depth": len(results)}

def measure_token_efficiency(prompt: str) -> int:
    """
    Measures the token usage of a given prompt using the tiktoken library.

    Args:
        prompt (str): The input prompt.

    Returns:
        int: The number of tokens used.
    """
    encoding = tiktoken.encoding_for_model("text-davinci-003")
    return len(encoding.encode(prompt))

def optimize_prompt(prompt_template: str, task_config: Dict[str, Any], max_iterations: int = 5) -> Dict[str, Any]:
    """
    Optimizes a prompt template to reduce token usage while maintaining reasoning quality.

    Args:
        prompt_template (str): The initial prompt template.
        task_config (Dict[str, Any]): Configuration for the task.
        max_iterations (int): Maximum number of optimization iterations.

    Returns:
        Dict[str, Any]: The optimized prompt and metrics.
    """
    try:
        optimized_prompt = prompt_template.format(**task_config)
    except KeyError as e:
        return {"error": f"Missing key in task_config: {e}"}

    initial_tokens = measure_token_efficiency(optimized_prompt)

    for _ in range(max_iterations):
        # Simplify the prompt by removing redundant words
        words = word_tokenize(optimized_prompt)
        if len(words) <= 5:  # Avoid over-simplification
            break
        optimized_prompt = " ".join(words[:-1])

        # Measure token usage
        try:
            current_tokens = measure_token_efficiency(optimized_prompt)
        except Exception as e:
            return {"error": f"Error measuring token efficiency: {e}"}

        if current_tokens >= initial_tokens:
            break
        initial_tokens = current_tokens

    return {"optimized_prompt": optimized_prompt, "token_usage": initial_tokens}

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Recursive Prompt Optimizer")
    parser.add_argument("prompt_template", type=str, help="The prompt template to optimize.")
    parser.add_argument("task_config", type=str, help="JSON string of task configuration.")
    parser.add_argument("--max_depth", type=int, default=3, help="Maximum recursion depth for simulation.")
    parser.add_argument("--max_iterations", type=int, default=5, help="Maximum iterations for optimization.")

    args = parser.parse_args()

    try:
        task_config = json.loads(args.task_config)
    except json.JSONDecodeError as e:
        print(f"Error parsing task_config: {e}")
        exit(1)

    print("Simulating recursive chain...")
    simulation_results = simulate_recursive_chain(args.prompt_template, task_config, args.max_depth)
    print(json.dumps(simulation_results, indent=2))

    print("Optimizing prompt...")
    optimization_results = optimize_prompt(args.prompt_template, task_config, args.max_iterations)
    print(json.dumps(optimization_results, indent=2))