# AI Code Review Pipeline

## Description
AI Code Review Pipeline is a Python tool that enables developers to streamline their code review process by integrating multiple AI reviewers. Users can define rules for different AI reviewers, aggregate their feedback, and apply filters to prioritize or categorize results. This makes the code review process more organized and tailored to specific project needs.

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/your-repo/ai-code-review-pipeline.git
    cd ai-code-review-pipeline
    ```

2. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

## Usage

Run the tool using the following command:

```bash
python ai_code_review_pipeline.py --file <path_to_code_file> --config <path_to_config_file> --filters <filter1> <filter2>
```

### Example

```bash
python ai_code_review_pipeline.py --file my_code.py --config reviewer_config.json --filters style performance
```

## Features

- **Integration with multiple AI code reviewers**: Supports configurable API endpoints for various AI reviewers.
- **Custom rules and filters**: Allows users to define filters to prioritize or categorize feedback.
- **Aggregated feedback**: Combines feedback from multiple reviewers into a structured format.
- **Error handling**: Handles missing files, network errors, and invalid configurations gracefully.

## Configuration

The configuration file should be a JSON file with the following structure:

```json
{
    "reviewers": [
        {
            "name": "Reviewer1",
            "api_url": "https://api.reviewer1.com/review",
            "api_key": "your_api_key_here"
        },
        {
            "name": "Reviewer2",
            "api_url": "https://api.reviewer2.com/review",
            "api_key": "your_api_key_here"
        }
    ]
}
```

## License
This project is licensed under the MIT License.