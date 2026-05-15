# Workflow AI Automator

## Description
Workflow AI Automator is a CLI tool designed to streamline repetitive business workflows by integrating Claude AI's text processing capabilities. Users can define workflows as JSON files with step-by-step instructions, and the tool automates these using Claude AI for tasks like summarization, email drafting, and decision-making.

## Installation

1. Clone the repository:
   ```
   git clone <repository_url>
   cd workflow_ai_automator
   ```

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage

Run the tool with the following command:
```
python workflow_ai_automator.py --workflow tasks.json --api-key <your_api_key>
```

### Example
Given a `tasks.json` file:
```json
{
    "steps": [
        {"task": "summarize", "input": "Summarize this text."},
        {"task": "email", "input": "Draft an email to the client."}
    ]
}
```
Run the tool:
```
python workflow_ai_automator.py --workflow tasks.json --api-key <your_api_key>
```

## Features
- **Customizable JSON-based workflows**: Define your business workflows in a simple JSON format.
- **Integration with Claude AI**: Automate tasks like summarization, email drafting, and decision-making.
- **Error handling and retry mechanism**: Handles missing files, invalid JSON, and network errors gracefully.

## License
This project is licensed under the MIT License.
