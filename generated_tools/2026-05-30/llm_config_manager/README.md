# LLM Config Manager

LLM Config Manager is a command-line tool designed to help AI developers manage and validate configuration files for open-source LLM frameworks like Llama.cpp. This tool simplifies the process of generating, validating, and updating configuration files, ensuring compatibility with popular frameworks.

## Features

- **Generate Configurations**: Quickly generate framework-specific configuration templates.
- **Validate Configurations**: Validate existing configuration files against predefined schemas.
- **Update Configurations**: Automatically update configuration parameters based on user input.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-repo/llm_config_manager.git
   cd llm_config_manager
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Generate a Configuration File
```bash
python llm_config_manager.py generate --template llama_cpp --output config.yaml
```

### Validate a Configuration File
```bash
python llm_config_manager.py validate --config config.yaml --schema llama_cpp
```

### Update a Configuration File
```bash
python llm_config_manager.py update --config config.yaml --updates "{learning_rate: 0.002, new_param: 'value'}"
```

## Example

1. Generate a configuration file for Llama.cpp:
   ```bash
   python llm_config_manager.py generate --template llama_cpp --output llama_config.yaml
   ```

2. Validate the generated configuration file:
   ```bash
   python llm_config_manager.py validate --config llama_config.yaml --schema llama_cpp
   ```

3. Update the configuration file:
   ```bash
   python llm_config_manager.py update --config llama_config.yaml --updates "{batch_size: 64}"
   ```

## License

This project is licensed under the MIT License.
