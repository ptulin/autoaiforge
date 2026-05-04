# AI Task Syncer

AI Task Syncer is a command-line tool that integrates with task management tools (e.g., Todoist) and uses Claude AI to analyze tasks, auto-prioritize them, and suggest deadlines. It can also extract action items from meeting notes and add them to the task manager.

## Features
- Syncs tasks from task management APIs (e.g., Todoist).
- Uses Claude AI to auto-prioritize tasks and suggest deadlines.
- Extracts action items from meeting notes or text files.
- Updates the task manager with prioritized tasks and suggestions.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-repo/ai_task_syncer.git
   cd ai_task_syncer
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Create a `.env` file in the project root and add your API keys:
   ```env
   TASK_MANAGER_API_KEY=your_task_manager_api_key
   CLAUDE_API_KEY=your_claude_api_key
   ```

## Usage

```bash
python ai_task_syncer.py --task-manager todoist --api-key your_api_key --meeting-notes notes.txt
```

### Arguments
- `--task-manager`: Task manager to sync with (e.g., `todoist`).
- `--api-key`: API key for the task manager (optional if provided in `.env`).
- `--meeting-notes`: Path to a text file containing meeting notes (optional).

## Example

```bash
python ai_task_syncer.py --task-manager todoist --meeting-notes meeting_notes.txt
```

## Testing

Run tests using `pytest`:

```bash
pytest test_ai_task_syncer.py
```

## Requirements
- Python 3.8+
- `requests==2.31.0`
- `openai==0.27.8`
- `python-dotenv==1.0.0`
- `pytest==7.4.2`

## License

This project is licensed under the MIT License.
