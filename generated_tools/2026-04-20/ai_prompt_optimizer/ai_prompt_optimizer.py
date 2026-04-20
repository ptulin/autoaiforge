import argparse
import json
import itertools
from jinja2 import Template
from nltk.tokenize import word_tokenize
from nltk.translate.bleu_score import sentence_bleu
import openai
import anthropic

def generate_permutations(prompt_template, variables):
    """Generate all permutations of the prompt template based on variables."""
    keys, values = zip(*variables.items())
    permutations = [dict(zip(keys, v)) for v in itertools.product(*values)]
    prompts = [Template(prompt_template).render(**perm) for perm in permutations]
    return prompts

def evaluate_response(response, reference):
    """Evaluate the response using a simple BLEU score against a reference."""
    try:
        response_tokens = word_tokenize(response)
        reference_tokens = [word_tokenize(reference)]
        return sentence_bleu(reference_tokens, response_tokens)
    except LookupError:
        import nltk
        nltk.download('punkt')
        response_tokens = word_tokenize(response)
        reference_tokens = [word_tokenize(reference)]
        return sentence_bleu(reference_tokens, response_tokens)

def get_ai_response(prompt, model, api_key):
    """Get AI response from the specified model."""
    try:
        if model == "gpt-5":
            openai.api_key = api_key
            completion = openai.Completion.create(
                engine="gpt-5-turbo",
                prompt=prompt,
                max_tokens=100
            )
            return completion.choices[0].text.strip()
        elif model == "claude-4.7":
            client = anthropic.Client(api_key)
            response = client.completion(
                prompt=anthropic.HUMAN_PROMPT + prompt + anthropic.AI_PROMPT,
                model="claude-4.7",
                max_tokens_to_sample=100
            )
            return response["completion"].strip()
        else:
            raise ValueError("Unsupported model: " + model)
    except Exception as e:
        return f"Error: {str(e)}"

def optimize_prompts(prompt_template, variables, reference, model, api_key):
    """Optimize prompts and evaluate their responses."""
    prompts = generate_permutations(prompt_template, variables)
    results = []

    for prompt in prompts:
        response = get_ai_response(prompt, model, api_key)
        if response.startswith("Error"):
            score = 0
        else:
            score = evaluate_response(response, reference)
        results.append({"prompt": prompt, "response": response, "score": score})

    results.sort(key=lambda x: x["score"], reverse=True)
    return results

def main():
    parser = argparse.ArgumentParser(description="AI Prompt Optimizer")
    parser.add_argument("--prompt-template", required=True, help="Path to the prompt template file")
    parser.add_argument("--variables", required=True, help="Path to the JSON file containing variables")
    parser.add_argument("--reference", required=True, help="Reference text for evaluation")
    parser.add_argument("--model", required=True, choices=["gpt-5", "claude-4.7"], help="AI model to use")
    parser.add_argument("--api-key", required=True, help="API key for the AI model")
    parser.add_argument("--output", required=True, help="Path to save the optimized prompts JSON file")

    args = parser.parse_args()

    try:
        with open(args.prompt_template, "r") as f:
            prompt_template = f.read()

        with open(args.variables, "r") as f:
            variables = json.load(f)

        results = optimize_prompts(prompt_template, variables, args.reference, args.model, args.api_key)

        with open(args.output, "w") as f:
            json.dump(results, f, indent=4)

        print(f"Optimized prompts saved to {args.output}")

    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()
