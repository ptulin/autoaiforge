import json
from typing import Callable, Dict, Any, List, Optional
from pydantic import BaseModel, ValidationError
import typer

app = typer.Typer()

class SkillMetadata(BaseModel):
    name: str
    description: str
    inputs: Dict[str, str]
    outputs: Dict[str, str]

class SkillRegistry:
    def __init__(self):
        self.skills: Dict[str, Dict[str, Any]] = {}

    def register_skill(self, func: Callable, metadata: SkillMetadata):
        if metadata.name in self.skills:
            raise ValueError(f"Skill with name '{metadata.name}' is already registered.")
        self.skills[metadata.name] = {
            "function": func,
            "metadata": metadata.dict()
        }

    def validate_skill(self, name: str, inputs: Dict[str, Any]) -> Dict[str, Any]:
        if name not in self.skills:
            raise ValueError(f"Skill '{name}' is not registered.")
        metadata = self.skills[name]["metadata"]
        for input_name, input_type in metadata["inputs"].items():
            if input_name not in inputs:
                raise ValueError(f"Missing required input: {input_name}")
            if not isinstance(inputs[input_name], eval(input_type)):
                raise ValueError(f"Input '{input_name}' must be of type {input_type}.")
        return inputs

    def execute_skill(self, name: str, inputs: Dict[str, Any]) -> Any:
        self.validate_skill(name, inputs)
        func = self.skills[name]["function"]
        return func(**inputs)

    def generate_registry_json(self, output_file: str):
        registry = {name: data["metadata"] for name, data in self.skills.items()}
        with open(output_file, "w") as f:
            json.dump(registry, f, indent=4)

    def generate_documentation(self, output_file: str):
        doc_lines = ["# Skill Registry Documentation\n"]
        for name, data in self.skills.items():
            metadata = data["metadata"]
            doc_lines.append(f"## {metadata['name']}")
            doc_lines.append(metadata["description"])
            doc_lines.append("### Inputs")
            for input_name, input_type in metadata["inputs"].items():
                doc_lines.append(f"- `{input_name}`: {input_type}")
            doc_lines.append("### Outputs")
            for output_name, output_type in metadata["outputs"].items():
                doc_lines.append(f"- `{output_name}`: {output_type}")
            doc_lines.append("")
        with open(output_file, "w") as f:
            f.write("\n".join(doc_lines))

registry = SkillRegistry()

def register_skill(func: Callable, metadata: Dict[str, Any]):
    try:
        skill_metadata = SkillMetadata(**metadata)
        registry.register_skill(func, skill_metadata)
    except ValidationError as e:
        raise ValueError(f"Invalid metadata: {e}")

@app.command()
def generate_registry(output_file: str):
    """Generate the skill registry JSON file."""
    registry.generate_registry_json(output_file)
    typer.echo(f"Skill registry JSON generated at {output_file}")

@app.command()
def generate_docs(output_file: str):
    """Generate the skill documentation."""
    registry.generate_documentation(output_file)
    typer.echo(f"Skill documentation generated at {output_file}")

if __name__ == "__main__":
    app()
