# Figma AI Sync Tool

## Description
The Figma AI Sync Tool integrates with the Figma API and AI models like OpenAI Codex to automate the export, optimization, and re-import of design elements. It enables developers to streamline updates to design systems and optimize layouts using AI.

## Installation

1. Clone the repository:
   ```bash
   git clone <repository_url>
   cd <repository_folder>
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up environment variables:
   Create a `.env` file in the project root and add:
   ```env
   OPENAI_API_KEY=<your_openai_api_key>
   ```

## Usage

Run the tool using the following command:
```bash
python figma_ai_sync.py --file-id <figma_file_id> --access-token <api_token> --optimize-layout
```

### Example:
```bash
python figma_ai_sync.py --file-id abc123 --access-token xyz456 --optimize-layout
```

## Features
- **Export Figma Design Elements**: Programmatically fetch design elements from Figma files.
- **AI-Driven Optimization**: Use OpenAI models to optimize layouts and styles.
- **Re-Import Updates**: Sync optimized design elements back to Figma.

## License
MIT License