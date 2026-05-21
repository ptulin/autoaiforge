# AI Email Generator

## Description
The AI Email Generator is a CLI tool designed to help users create professional-quality business emails using generative AI models like OpenAI's GPT. Users can specify the tone, purpose, and key points for the email, making it ideal for automating repetitive email creation tasks.

## Features
- Generate emails with a specified tone (e.g., formal, casual).
- Specify the purpose of the email (e.g., follow-up, introduction).
- Include key points to be addressed in the email.
- Save the generated email to a file or display it directly in the terminal.

## Installation
1. Clone the repository:
   ```bash
   git clone <repository-url>
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage
1. Set the `OPENAI_API_KEY` environment variable with your OpenAI API key.
   ```bash
   export OPENAI_API_KEY=your_api_key_here
   ```
2. Run the CLI tool:
   ```bash
   python ai_email_generator.py --tone "formal" --purpose "follow-up" --key_points "meeting recap, next steps" --output_file "email.txt"
   ```

   - `--tone`: Tone of the email (e.g., formal, casual).
   - `--purpose`: Purpose of the email (e.g., follow-up, introduction).
   - `--key_points`: Key points to include in the email.
   - `--output_file`: (Optional) File to save the generated email.

## Testing
Run the tests using `pytest`:
```bash
pytest test_ai_email_generator.py
```

## License
MIT License
