import os
import argparse
import hashlib
from pygments import highlight
from pygments.lexers import guess_lexer_for_filename
from pygments.formatters import HtmlFormatter

def embed_watermark(content, watermark):
    """
    Embed a watermark into the source code by appending it as a comment.
    """
    watermark_comment = f"# Watermark: {watermark}"
    return f"{content}\n{watermark_comment}"

def generate_watermark(identifier):
    """
    Generate a unique watermark using a hash of the identifier.
    """
    return hashlib.sha256(identifier.encode()).hexdigest()

def process_file(file_path, output_dir, watermark):
    """
    Process a single file to embed a watermark.
    """
    try:
        with open(file_path, 'r') as f:
            content = f.read()

        watermarked_content = embed_watermark(content, watermark)

        output_path = os.path.join(output_dir, os.path.basename(file_path))
        with open(output_path, 'w') as f:
            f.write(watermarked_content)

        print(f"Watermarked file saved to {output_path}")
    except Exception as e:
        print(f"Error processing file {file_path}: {e}")

def process_directory(input_dir, output_dir, watermark):
    """
    Process all files in a directory to embed watermarks.
    """
    for root, _, files in os.walk(input_dir):
        for file in files:
            file_path = os.path.join(root, file)
            process_file(file_path, output_dir, watermark)

def main():
    parser = argparse.ArgumentParser(description="AI Code Watermarker embeds invisible watermarks in source code files.")
    parser.add_argument('--input', required=True, help="Input file or directory containing source code.")
    parser.add_argument('--output', required=True, help="Output directory for watermarked source code.")
    parser.add_argument('--identifier', required=True, help="Unique identifier for generating the watermark.")

    args = parser.parse_args()

    input_path = args.input
    output_dir = args.output
    identifier = args.identifier

    watermark = generate_watermark(identifier)

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    if os.path.isfile(input_path):
        process_file(input_path, output_dir, watermark)
    elif os.path.isdir(input_path):
        process_directory(input_path, output_dir, watermark)
    else:
        print("Invalid input path. Please provide a valid file or directory.")

if __name__ == "__main__":
    main()
