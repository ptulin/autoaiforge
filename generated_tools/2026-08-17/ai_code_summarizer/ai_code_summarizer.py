import argparse
import ast
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer


def summarize_code(code):
    try:
        # Initialize model and tokenizer
        model = AutoModelForSeq2SeqLM.from_pretrained('t5-small')
        tokenizer = AutoTokenizer.from_pretrained('t5-small')

        # Parse code into abstract syntax tree
        tree = ast.parse(code)

        # Convert tree to string
        code_str = ast.unparse(tree)

        # Tokenize code
        inputs = tokenizer(code_str, return_tensors='pt')

        # Generate summary
        outputs = model.generate(inputs['input_ids'], num_beams=4, no_repeat_ngram_size=2, min_length=30, max_length=100, early_stopping=True)

        # Convert summary to string
        summary = tokenizer.decode(outputs[0], skip_special_tokens=True)

        return summary
    except SyntaxError as e:
        return str(e)
    except Exception as e:
        return str(e)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='AI Code Summarizer')
    parser.add_argument('--file', type=str, help='Path to Python code file')
    args = parser.parse_args()

    if args.file:
        with open(args.file, 'r') as f:
            code = f.read()
            summary = summarize_code(code)
            print(summary)