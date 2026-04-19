# Claude Design Prototype Generator

## Description
The Claude Design Prototype Generator is a command-line tool that allows developers to generate UI/UX prototypes by providing descriptive text prompts. It leverages Anthropic's Claude Design API to automate the creation of wireframes and interactive prototypes, streamlining the design process.

## Features
- Generate UI/UX prototypes from descriptive text prompts.
- Export designs in JSON or PNG formats.
- Easily integrate with popular design tools like Figma via plugins.

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/claude_design_prototype_generator.git
   cd claude_design_prototype_generator
   ```
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage
1. Set your Claude API key as an environment variable:
   ```bash
   export CLAUDE_API_KEY="your_api_key"
   ```
2. Run the tool with a text prompt:
   ```bash
   python claude_design_prototype_generator.py --prompt "Create a login page with email and password fields and a submit button" --output-format json --output-file output.json
   ```
3. The generated prototype will be saved to the specified output file.

## Example
```bash
python claude_design_prototype_generator.py --prompt "Create a dashboard with charts and a navigation bar" --output-format png --output-file dashboard.png
```

## Requirements
- Python 3.7+
- `requests==2.31.0`
- `pytest==7.4.2`

## Testing
Run the tests using pytest:
```bash
pytest test_claude_design_prototype_generator.py
```

## Notes
- Ensure you have a valid API key for the Claude Design API.
- The tool requires an active internet connection to communicate with the API.

## License
This project is licensed under the MIT License.