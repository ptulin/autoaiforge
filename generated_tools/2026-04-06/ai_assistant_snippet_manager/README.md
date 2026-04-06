# AI Assistant Snippet Manager

## Description
The AI Assistant Snippet Manager is a CLI tool that bridges the gap between AI coding assistants like OpenAI's ChatGPT and your development workflow. It allows you to query AI for code snippets, save them with context-aware metadata, and retrieve them later for reuse. This tool is perfect for managing frequently used code patterns and templates.

## Features
- Query AI coding assistants for code snippets via CLI.
- Save generated snippets with auto-tagging and metadata.
- Retrieve and reuse saved snippets based on tags.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-repo/ai_assistant_snippet_manager.git
   cd ai_assistant_snippet_manager
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Query AI and Save Snippets
To query the AI assistant for a code snippet and save it with tags:
```bash
python ai_assistant_snippet_manager.py --query "create a Python class for database handling" --save --tags "database,ORM" --api-key YOUR_OPENAI_API_KEY
```

### Retrieve Snippets
To retrieve saved snippets by tags:
```bash
python ai_assistant_snippet_manager.py --retrieve "database" --db-path snippets.db
```

### Options
- `--query`: Query to send to the AI assistant.
- `--save`: Save the generated snippet.
- `--tags`: Comma-separated tags for the snippet (required with `--save`).
- `--retrieve`: Retrieve snippets by tags.
- `--api-key`: OpenAI API key (required for querying AI).
- `--db-path`: Path to the SQLite database (default: `snippets.db`).

## Example
Generate and save a snippet:
```bash
python ai_assistant_snippet_manager.py --query "write a function to calculate factorial" --save --tags "math,factorial" --api-key YOUR_OPENAI_API_KEY
```

Retrieve snippets with the tag `math`:
```bash
python ai_assistant_snippet_manager.py --retrieve "math" --db-path snippets.db
```

## License
MIT License