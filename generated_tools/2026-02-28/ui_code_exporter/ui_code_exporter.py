import argparse
import json
import os
import svgwrite
import openai

def parse_design_file(input_file):
    """Parse the input design file (JSON or SVG) into structured components."""
    if input_file.endswith('.json'):
        try:
            with open(input_file, 'r') as f:
                return json.load(f)
        except json.JSONDecodeError:
            raise ValueError("Invalid JSON file.")
    elif input_file.endswith('.svg'):
        try:
            with open(input_file, 'r') as f:
                return f.read()
        except FileNotFoundError:
            raise ValueError("SVG file not found.")
    else:
        raise ValueError("Unsupported file format. Only JSON and SVG are supported.")

def generate_code_with_ai(design_data, framework):
    """Generate front-end code using OpenAI Codex based on the design data."""
    prompt = f"Generate {framework} front-end code (HTML, CSS, JS) based on the following design data:\n{design_data}"
    try:
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=1500
        )
        return response['choices'][0]['text'].strip()
    except openai.error.OpenAIError as e:
        raise RuntimeError(f"Failed to generate code: {e}")

def save_code(output_dir, code, framework):
    """Save the generated code into the specified output directory."""
    os.makedirs(output_dir, exist_ok=True)
    if framework == "react":
        file_name = os.path.join(output_dir, "Component.jsx")
    elif framework == "vue":
        file_name = os.path.join(output_dir, "Component.vue")
    else:
        file_name = os.path.join(output_dir, "index.html")

    with open(file_name, 'w') as f:
        f.write(code)

def main():
    parser = argparse.ArgumentParser(description="UI Code Exporter: Generate front-end code from design files.")
    parser.add_argument('--input', required=True, help="Path to the input design file (JSON or SVG).")
    parser.add_argument('--framework', choices=['react', 'vue', 'html'], default='html', help="Framework for the generated code.")
    parser.add_argument('--output', required=True, help="Path to the output directory.")

    args = parser.parse_args()

    try:
        design_data = parse_design_file(args.input)
        generated_code = generate_code_with_ai(design_data, args.framework)
        save_code(args.output, generated_code, args.framework)
        print(f"Code successfully generated and saved to {args.output}.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()