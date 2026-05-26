# Claude Plugin Deployer

Claude Plugin Deployer is a command-line tool designed to simplify the process of managing and deploying plugins for Claude AI. This tool provides a unified interface for generating, testing, and deploying plugins, making it easier for AI developers to adapt Claude AI's capabilities to specific use cases.

## Features

- Unified CLI for managing Claude AI plugins
- Validation of plugin configurations before deployment
- Auto-versioning and rollback options for plugin updates
- Seamless integration with Claude AI plugin ecosystem

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-repo/claude_plugin_deployer.git
   cd claude_plugin_deployer
   ```
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Deploy a Plugin

To deploy a plugin, provide the path to the plugin configuration file (in TOML format):

```bash
python claude_plugin_deployer.py deploy --plugin config.toml
```

### Test and Deploy a Plugin

To test the plugin before deploying it, use the `--test` flag:

```bash
python claude_plugin_deployer.py deploy --plugin config.toml --test
```

## Example Configuration File

```toml
[plugin]
name = "example_plugin"
version = "1.0.0"
```

## Development

### Running Tests

To run the test suite, use pytest:

```bash
pytest
```

## License

This project is licensed under the MIT License.