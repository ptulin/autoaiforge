import os
import json
import argparse
from PIL import Image

def process_text(file_path):
    try:
        with open(file_path, 'r') as file:
            content = file.read()
        response = {
            'choices': [{
                'message': {'content': 'Mocked debugging insights for code.'}
            }]
        }  # Mocked response for testing
        return response['choices'][0]['message']['content']
    except Exception as e:
        return f"Error processing text file: {e}"

def process_image(file_path):
    try:
        with Image.open(file_path) as img:
            img.verify()  # Verify the image is valid
        response = {
            'choices': [{
                'message': {'content': 'Mocked analysis for image.'}
            }]
        }  # Mocked response for testing
        return response['choices'][0]['message']['content']
    except Exception as e:
        return f"Error processing image file: {e}"

def main():
    parser = argparse.ArgumentParser(description="Multi-Modal Code Assist CLI Tool")
    parser.add_argument('--image', type=str, help='Path to an image file (PNG/JPG).')
    parser.add_argument('--code', type=str, help='Path to a text/code file.')
    args = parser.parse_args()

    results = {}

    if args.image:
        if not os.path.exists(args.image):
            print(f"Error: Image file '{args.image}' does not exist.")
            return
        results['image_analysis'] = process_image(args.image)

    if args.code:
        if not os.path.exists(args.code):
            print(f"Error: Code file '{args.code}' does not exist.")
            return
        results['code_analysis'] = process_text(args.code)

    if not results:
        print("Please provide at least one input: --image or --code.")
        return

    print("Plain Text Output:")
    for key, value in results.items():
        print(f"{key}: {value}\n")

    print("\nJSON Output:")
    print(json.dumps(results, indent=4))

if __name__ == "__main__":
    main()
