import argparse
import yaml
import jsonschema
import os

# Predefined schema for validation
SCHEMAS = {
    "llama_cpp": {
        "type": "object",
        "properties": {
            "model": {"type": "string"},
            "learning_rate": {"type": "number", "minimum": 0},
            "batch_size": {"type": "integer", "minimum": 1}
        },
        "required": ["model", "learning_rate", "batch_size"]
    }
}

# Predefined templates for configuration
TEMPLATES = {
    "llama_cpp": {
        "model": "path/to/your/model.bin",
        "learning_rate": 0.001,
        "batch_size": 32
    }
}

def generate_config(template_name, output_path):
    """Generate a configuration file based on a predefined template."""
    if template_name not in TEMPLATES:
        raise ValueError(f"Unknown template: {template_name}")

    with open(output_path, 'w') as f:
        yaml.dump(TEMPLATES[template_name], f)

    print(f"Configuration file generated at {output_path}")

def validate_config(config_path, schema_name):
    """Validate a configuration file against a predefined schema."""
    if schema_name not in SCHEMAS:
        raise ValueError(f"Unknown schema: {schema_name}")

    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)

    schema = SCHEMAS[schema_name]
    jsonschema.validate(instance=config, schema=schema)

    print(f"Configuration file {config_path} is valid.")

def update_config(config_path, updates):
    """Update a configuration file with new parameters."""
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"Configuration file {config_path} not found.")

    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)

    config.update(updates)

    with open(config_path, 'w') as f:
        yaml.dump(config, f)

    print(f"Configuration file {config_path} updated.")

def main():
    parser = argparse.ArgumentParser(description="LLM Config Manager")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Generate subcommand
    generate_parser = subparsers.add_parser("generate", help="Generate a configuration file")
    generate_parser.add_argument("--template", required=True, help="Template name (e.g., llama_cpp)")
    generate_parser.add_argument("--output", required=True, help="Output file path")

    # Validate subcommand
    validate_parser = subparsers.add_parser("validate", help="Validate a configuration file")
    validate_parser.add_argument("--config", required=True, help="Path to the configuration file")
    validate_parser.add_argument("--schema", required=True, help="Schema name (e.g., llama_cpp)")

    # Update subcommand
    update_parser = subparsers.add_parser("update", help="Update a configuration file")
    update_parser.add_argument("--config", required=True, help="Path to the configuration file")
    update_parser.add_argument("--updates", required=True, help="Updates in YAML format")

    args = parser.parse_args()

    try:
        if args.command == "generate":
            generate_config(args.template, args.output)
        elif args.command == "validate":
            validate_config(args.config, args.schema)
        elif args.command == "update":
            updates = yaml.safe_load(args.updates)
            update_config(args.config, updates)
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()