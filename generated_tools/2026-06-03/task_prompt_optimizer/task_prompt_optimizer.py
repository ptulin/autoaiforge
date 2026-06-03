import argparse
import logging
import openai

def optimize_prompt(api_key, input_prompt, iterations):
    """
    Optimize a given prompt by iteratively refining it based on agent feedback.

    Args:
        api_key (str): OpenAI API key.
        input_prompt (str): Initial prompt to optimize.
        iterations (int): Number of refinement iterations.

    Returns:
        str: The optimized prompt.
    """
    openai.api_key = api_key

    current_prompt = input_prompt
    logging.info("Starting prompt optimization")

    for i in range(iterations):
        try:
            logging.info(f"Iteration {i + 1}: Sending prompt to OpenAI API")
            response = openai.Completion.create(
                engine="text-davinci-003",
                prompt=f"Optimize this prompt for clarity and effectiveness: {current_prompt}",
                max_tokens=100
            )
            optimized_prompt = response.choices[0].text.strip()
            logging.info(f"Iteration {i + 1}: Received optimized prompt")

            if optimized_prompt == current_prompt:
                logging.info("No further optimization possible. Stopping early.")
                break

            current_prompt = optimized_prompt
        except openai.error.OpenAIError as e:
            logging.error(f"OpenAI API error: {e}")
            break

    logging.info("Prompt optimization completed")
    return current_prompt

def main():
    parser = argparse.ArgumentParser(description="Task Prompt Optimizer")
    parser.add_argument("--api_key", required=True, help="OpenAI API key")
    parser.add_argument("--input_prompt", required=True, help="Initial prompt to optimize")
    parser.add_argument("--iterations", type=int, default=5, help="Number of refinement iterations")

    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

    optimized_prompt = optimize_prompt(args.api_key, args.input_prompt, args.iterations)

    print("Optimized Prompt:")
    print(optimized_prompt)

if __name__ == "__main__":
    main()