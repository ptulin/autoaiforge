import argparse
import json
import time
import pandas as pd
from nltk.translate.bleu_score import sentence_bleu
from openai import ChatCompletion
from anthropic import Client

def load_dataset(file_path):
    if str(file_path).endswith('.json'):
        with open(file_path, 'r') as f:
            return json.load(f)
    elif str(file_path).endswith('.csv'):
        return pd.read_csv(file_path).to_dict('records')
    else:
        raise ValueError("Unsupported file format. Use JSON or CSV.")

def evaluate_model_responses(prompts, model_name, generate_response):
    metrics = []
    for prompt_data in prompts:
        prompt = prompt_data['prompt']
        reference = prompt_data.get('reference', None)

        start_time = time.time()
        try:
            response = generate_response(prompt)
        except Exception as e:
            response = f"Error: {str(e)}"
        latency = time.time() - start_time

        response_length = len(response)
        bleu_score = sentence_bleu([reference.split()], response.split()) if reference else None

        metrics.append({
            'prompt': prompt,
            'response': response,
            'latency': latency,
            'response_length': response_length,
            'bleu_score': bleu_score
        })

    return metrics

def generate_gpt5_response(prompt):
    response = ChatCompletion.create(
        model="gpt-5",
        messages=[{"role": "user", "content": prompt}]
    )
    return response['choices'][0]['message']['content']

def generate_claude47_response(prompt):
    client = Client(api_key="YOUR_ANTHROPIC_API_KEY")
    response = client.completion(
        prompt=prompt,
        model="claude-4.7",
        max_tokens=500
    )
    return response['completion']

def generate_report(metrics_gpt5, metrics_claude, output_file):
    report = {
        'GPT-5': metrics_gpt5,
        'Claude-4.7': metrics_claude
    }

    if str(output_file).endswith('.json'):
        with open(output_file, 'w') as f:
            json.dump(report, f, indent=4)
    elif str(output_file).endswith('.html'):
        html_content = "<html><head><title>AI Model Benchmark Report</title></head><body>"
        html_content += "<h1>AI Model Benchmark Report</h1>"
        for model, metrics in report.items():
            html_content += f"<h2>{model}</h2><table border='1'>"
            html_content += "<tr><th>Prompt</th><th>Response</th><th>Latency</th><th>Response Length</th><th>BLEU Score</th></tr>"
            for metric in metrics:
                html_content += f"<tr><td>{metric['prompt']}</td><td>{metric['response']}</td><td>{metric['latency']:.2f}</td><td>{metric['response_length']}</td><td>{metric['bleu_score']}</td></tr>"
            html_content += "</table>"
        html_content += "</body></html>"

        with open(output_file, 'w') as f:
            f.write(html_content)
    else:
        raise ValueError("Unsupported output format. Use JSON or HTML.")

def main():
    parser = argparse.ArgumentParser(description="AI Model Benchmark Tool")
    parser.add_argument('--dataset', required=True, help="Path to the dataset file (JSON or CSV)")
    parser.add_argument('--output', required=True, help="Path to the output report file (JSON or HTML)")
    args = parser.parse_args()

    try:
        prompts = load_dataset(args.dataset)
    except Exception as e:
        print(f"Error loading dataset: {str(e)}")
        return

    try:
        metrics_gpt5 = evaluate_model_responses(prompts, "GPT-5", generate_gpt5_response)
        metrics_claude = evaluate_model_responses(prompts, "Claude-4.7", generate_claude47_response)
        generate_report(metrics_gpt5, metrics_claude, args.output)
        print(f"Benchmark report generated: {args.output}")
    except Exception as e:
        print(f"Error during benchmarking: {str(e)}")

if __name__ == "__main__":
    main()
