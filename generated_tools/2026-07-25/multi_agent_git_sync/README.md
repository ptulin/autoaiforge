# Multi-Agent Git Sync

## Description
Multi-Agent Git Sync is a CLI tool designed to coordinate multiple AI coding agents working on the same Git repository. It provides functionality for file locking, branch management, and AI-assisted merge conflict resolution, ensuring smooth collaboration in shared codebases.

## Features
- **File Locking**: Prevent overwrite collisions by locking files.
- **Branch Management**: Automate branch creation and assignment.
- **AI-Assisted Merge Conflict Resolution**: Resolve merge conflicts intelligently using AI-based heuristics.

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/your-repo/multi_agent_git_sync.git
   cd multi_agent_git_sync
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage
```bash
python multi_agent_git_sync.py --repo /path/to/repo --agent agent_1 --task lock --file test_file.py
python multi_agent_git_sync.py --repo /path/to/repo --agent agent_1 --task unlock --file test_file.py
python multi_agent_git_sync.py --repo /path/to/repo --agent agent_1 --task branch --branch new_feature_branch
python multi_agent_git_sync.py --repo /path/to/repo --agent agent_1 --task resolve --base_branch main --feature_branch feature
```

## Example
Lock a file:
```bash
python multi_agent_git_sync.py --repo /path/to/repo --agent agent_1 --task lock --file test_file.py
```

## Testing
Run the tests using pytest:
```bash
pytest test_multi_agent_git_sync.py
```