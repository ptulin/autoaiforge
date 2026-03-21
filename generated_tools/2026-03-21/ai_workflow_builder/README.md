# AI Workflow Builder

## Description
AI Workflow Builder allows developers to define and execute custom automation workflows by chaining AI model outputs (like OpenAI's GPT models) with traditional tasks (e.g., API calls, data processing). It uses a declarative YAML configuration file to define the sequence of tasks, making it easy to create and modify workflows without writing additional code.

## Features
- Supports chaining AI model responses with other tasks
- Declarative YAML-based workflow configuration
- Built-in support for error handling and retries

## Installation
1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd <repository-folder>
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage
1. Create a YAML configuration file (e.g., `workflow.yaml`) with the following structure:
   ```yaml
   workflow:
     - name: "Step 1"
       type: "ai_task"
       prompt: "Write a poem about AI."
       model: "text-davinci-003"
       max_tokens: 50
   ```

2. Run the tool:
   ```bash
   python ai_workflow_builder.py --config workflow.yaml --output results.yaml
   ```

3. Check the output in the terminal or in the specified output file (e.g., `results.yaml`).

## Example Workflow
```yaml
workflow:
  - name: "Generate AI Response"
    type: "ai_task"
    prompt: "What are the benefits of AI in healthcare?"
    model: "text-davinci-003"
    max_tokens: 100
```

## Testing
Run the tests using pytest:
```bash
pytest test_ai_workflow_builder.py
```

## License
This project is licensed under the MIT License.
