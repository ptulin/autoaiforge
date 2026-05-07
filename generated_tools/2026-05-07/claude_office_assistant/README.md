# Claude Office Assistant

This Python tool provides an API wrapper that connects Claude AI with Microsoft Office files (Word, Excel, and PowerPoint). It allows developers to automate tasks like summarizing documents, generating presentation slides from text, and analyzing Excel data.

## Features

- **Summarize Word Documents**: Extract and summarize the content of `.docx` files using Claude AI.
- **Analyze Excel Files**: Analyze `.xlsx` files and return basic statistics like row and column counts.
- **Generate PowerPoint Presentations**: Create `.pptx` presentations from plain text input.

## Requirements

Install the following Python packages:

```
pip install python-docx openpyxl python-pptx openai
```

## Usage

Run the tool from the command line:

### Summarize a Word Document

```
python claude_office_assistant.py --file path/to/document.docx --summarize --api_key YOUR_API_KEY
```

### Analyze an Excel File

```
python claude_office_assistant.py --file path/to/spreadsheet.xlsx --analyze
```

### Generate a PowerPoint Presentation

```
python claude_office_assistant.py --generate "Title1\nContent1\n\nTitle2\nContent2" --output path/to/output.pptx
```

## Testing

Run the tests using `pytest`:

```
pytest test_claude_office_assistant.py
```

## License

MIT License