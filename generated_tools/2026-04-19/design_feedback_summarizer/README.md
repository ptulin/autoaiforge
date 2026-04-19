# Design Feedback Summarizer

## Description
The **Design Feedback Summarizer** is a Python library that helps developers analyze and summarize feedback for UI/UX designs. By leveraging Anthropic's Claude API, the tool generates concise summaries and actionable recommendations for iterative improvements. It supports input from multiple sources, such as JSON and plain text files, and outputs the results in either JSON or plain text format.

## Features
- Summarizes large volumes of design feedback.
- Extracts actionable insights for iterative improvements.
- Supports input from JSON or plain text files.
- Outputs results in JSON or plain text format.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-repo/design-feedback-summarizer.git
   cd design-feedback-summarizer
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### As a Library
```python
from design_feedback_summarizer import summarize_feedback

# Summarize feedback from a JSON file
result = summarize_feedback("feedback.json")
print(result)

# Summarize feedback from a text file and save output to a file
summarize_feedback("feedback.txt", output_file="summary.txt", output_format="text")
```

### As a CLI Tool
```bash
python design_feedback_summarizer.py feedback.json --output_file summary.json --output_format json
```

## Example Input and Output

### Input (JSON file):
```json
[
    "Great design!",
    "Navigation is confusing.",
    "Add more color themes."
]
```

### Output (JSON):
```json
{
    "summary": "Users appreciate the clean design but find navigation confusing.",
    "recommendations": [
        "Improve navigation clarity by adding labels to icons.",
        "Provide a tutorial for first-time users."
    ]
}
```

## Testing

Run the tests using `pytest`:
```bash
pytest test_design_feedback_summarizer.py
```

## License
MIT License
