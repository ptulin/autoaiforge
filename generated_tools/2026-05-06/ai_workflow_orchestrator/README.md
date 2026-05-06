# AI Workflow Orchestrator

AI Workflow Orchestrator is a Python library for designing and running customizable AI-powered workflow automation pipelines. It allows developers to chain together AI API calls, such as Claude AI or Oxygen AI, as well as other custom Python functions, into modular and reusable workflows.

## Features

- Define modular AI workflows with YAML or Python
- Integrate multiple AI APIs like Claude AI or Oxygen AI
- Error handling and retries for API calls

## Installation

Install the required dependencies:

```bash
pip install -r requirements.txt
```

## Usage

Create a YAML file defining your workflow, for example, `workflow.yaml`:

```yaml
step1:
  type: api_call
  url: http://example.com/api
  payload:
    key: value
```

Run the orchestrator with the following command:

```bash
python ai_workflow_orchestrator.py --workflow workflow.yaml
```

## Example Workflow

```yaml
step1:
  type: api_call
  url: http://example.com/api
  payload:
    key: value
step2:
  type: python_function
  function: some_python_function
  args:
    - arg1
    - arg2
  kwargs:
    kwarg1: value1
    kwarg2: value2
```

## Error Handling

- API calls are retried up to 3 times with a 2-second delay between attempts.
- Errors are captured and included in the workflow results.

## License

MIT License