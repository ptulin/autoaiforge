import argparse
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

def complete_code(input_code, model_name='codebert-base'):
    model = AutoModelForCausalLM.from_pretrained(model_name)
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    if not input_code:
        return ''
    inputs = tokenizer(input_code, return_tensors='pt')
    outputs = model.generate(**inputs, max_length=512)
    completed_code = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return completed_code

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='AI Code Completion Tool')
    parser.add_argument('--input', type=str, help='Input code file or string')
    parser.add_argument('--output', type=str, help='Output completed code file or string')
    args = parser.parse_args()
    if args.input and args.output:
        with open(args.input, 'r') as f:
            input_code = f.read()
        completed_code = complete_code(input_code)
        with open(args.output, 'w') as f:
            f.write(completed_code)
    else:
        parser.print_help()