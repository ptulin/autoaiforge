import os
import sys
import argparse

# Constants
TEMPLATES = {
    "python": {
        "flask": {
            "auth": """from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/login', methods=['POST'])
def login():
    return jsonify({'message': 'Login endpoint'})

if __name__ == '__main__':
    app.run(debug=True)
""",
            "base": """from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return "Hello, Flask!"

if __name__ == '__main__':
    app.run(debug=True)
"""
        }
    }
}

def generate_project(language, framework, features, output):
    """Generates a project scaffold based on user input."""
    try:
        # Ensure output directory exists
        os.makedirs(output, exist_ok=True)

        # Parse features
        feature_list = [f.strip().lower() for f in features.split(',') if f.strip()]

        # Generate files based on templates
        if language in TEMPLATES and framework in TEMPLATES[language]:
            framework_templates = TEMPLATES[language][framework]

            # Select template based on features
            template_key = 'auth' if 'auth' in feature_list else 'base'
            template_content = framework_templates.get(template_key, '')

            if template_content:
                # Write main file
                main_file_path = os.path.join(output, 'app.py')
                with open(main_file_path, 'w') as f:
                    f.write(template_content)

                print(f"Project generated successfully in '{output}'")
            else:
                print("No matching template found for the specified features.")
        else:
            print("Language or framework not supported.")
    except Exception as e:
        print(f"Error generating project: {e}")


def main():
    parser = argparse.ArgumentParser(description="Generate a project scaffold based on user input.")
    parser.add_argument('--language', required=True, choices=['python'], help='Programming language')
    parser.add_argument('--framework', required=True, choices=['flask'], help='Framework')
    parser.add_argument('--features', default='', help='Comma-separated list of features (e.g., auth)')
    parser.add_argument('--output', default='generated_project', help='Output directory for the generated project')

    args = parser.parse_args()

    generate_project(args.language, args.framework, args.features, args.output)

if __name__ == '__main__':
    main()